# Blog Website

A simple blog website using Python, HTML, Flask, SQLAlchemy and using the Bootstrap 'Clean Blog' theme.

### To install

```
pip install -r requirements.txt  # install dependencies
```

**Note**:
ln. 16 in main.py uses an environment varialbe for the app's secret key. You will need to set this up to run the app.

Run main.py and view the website at 'http://localhost:5000'.

## Functionality

### Home Page
All the blog posts are shown on the home page. There is an older posts button, but I have not added its functionality. From the home page, blog titles, subtitles, authors and dates are displayed, and individual blogs can be clicked on to go to the specific blog's page. The admin user can also delete posts from the home page.

### Creating Posts
Creating posts can only be done by the admin User. This is the user with id = 1 in the user database, which is the first user registered. Creating posts is done using a form, with entries for title, subtitle, a URL for the background image, and the post content. Author and creation date are added to the database automatically.

### Edit Posts
The admin user can also edit existing posts while on that post's page. This uses the same form as with creating posts, with the original content auto-filled.

### Comment on Posts
All logged in users can post comments to blog posts, and also remove their own comments. Admin users can also delete any comments.

### Navigation
The navigation bar includes links to register or login for logged-out users, or a link to log out for logged in users. There is a link to an About page and a Contact page, which aren't used.

## Pictures / Demo

