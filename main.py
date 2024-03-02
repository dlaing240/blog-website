from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
import os

app = Flask(__name__)  # Create instance of the Flask class
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')


ckeditor = CKEditor(app)  # Initialise CKEditor for text editing and integrating it with Flask app.
Bootstrap5(app)  # Initialise Bootstrap

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
    return db.get_or_404(User, user)


# Initialise gravatar to give users profile avatars
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=False,
                    base_url=None)


# Create database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URO", 'sqlite:///posts.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Users database
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


# Posts database
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments = relationship("Comment", back_populates="post", cascade='all, delete')


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    post = relationship("BlogPost", back_populates="comments")


with app.app_context():
    db.create_all()


# Decorator to implement admin-only permissions
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # The first user in the database is chosen to be the admin user
            if current_user.id == 1:
                return f(*args, **kwargs)
        else:
            return abort(code=404)
    return decorated_function

# Admin user for demonstration:
# email: Admin@email
# username: Admin
# password: demo


# Hash the user's password when creating a new user using Werkzeug
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data, method="scrypt", salt_length=16)
        email = form.email.data
        # Ensure email is unique
        if User.query.filter_by(email=email).first():
            flash("A user already exists with that email!")
            return redirect(url_for('login'))
        # Create new User
        new_user = User()
        new_user.username = form.username.data
        new_user.email = email
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


# Retrieve a user from the database based on their email.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # flash error if email is not found in the database
        if not user:
            flash("Email not recognised.")
            return redirect(url_for('login'))
        # Otherwise the password is checked and if successful the user is logged in
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('get_all_posts'))
        else:
            flash("Incorrect Password")
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


# Currently all posts are displayed on the home page
@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# Page to show full individual posts
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        # Allow signed in users to leave comments on posts
        if not current_user.is_authenticated:
            flash("You must be logged in to leave comments!")
            return redirect(url_for('login'))
        # Create a new comment from the comment form, and add it to the database
        new_comment = Comment()
        new_comment.text = comment_form.comment.data
        new_comment.comment_author = current_user
        new_comment.post = requested_post
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))
    return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)


# Only admins can add new posts
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Only admins can edit posts
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# Only admins can delete posts
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/comment_delete/<int:comment_id>")
def delete_comment(comment_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    post = comment_to_delete.post_id
    if current_user.is_authenticated:
        if current_user == comment_to_delete.comment_author:
            db.session.delete(comment_to_delete)
            db.session.commit()
            return redirect(url_for('show_post', post_id=post))
    return redirect(url_for('show_post', post_id=post))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False)
