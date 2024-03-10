# Blog Website

A simple blog website using Python, HTML, Flask and SQLAlchemy. The Bootstrap 'Clean Blog' theme was used for styling and javascript.

### To install
Clone the repository and then install dependencies
```
pip install -r requirements.txt  # install dependencies
```

**Note**:
Line 16 in main.py uses an environment varialbe for the app's secret key. You will need to set this up to run the app. There is also an environment variable for the database, but an SQlite database will be automatically created in its absence.

Run main.py and view the website at 'http://localhost:5000'.

## Functionality

### Home Page
All the blog posts are shown on the home page. There is an 'older posts' button, but I have not added its functionality. From the home page, blog titles, subtitles, authors and dates are displayed, and individual blogs can be clicked on to go to the specific blog's page. The admin user can also delete posts from the home page.

### Creating Posts
Creating posts can only be done by the admin User. This is the user with id = 1 in the user database, which is the first user registered. Creating posts is done using a form, with entries for title, subtitle, a URL for the background image, and the post content. Author and creation date are added to the database automatically.

### Edit Posts
The admin user can also edit existing posts while on that post's page. This uses the same form as creating posts, with the original content auto-filled.

### Comment on Posts
All logged in users can post comments to blog posts, and also remove their own comments. Admin users can also delete any comments.

### Navigation
The navigation bar includes links to register or login for logged-out users, or a link to log out for logged in users. There is a link to an About page and a Contact page, which aren't used.

## Preview / Pictures
### Home Page
![home-page](https://github.com/dlaing240/blog-website/assets/159714200/4c90ac1b-c24c-48e9-9b45-cbc718f56a22)
### Create post
![create-post](https://github.com/dlaing240/blog-website/assets/159714200/f2615c37-b596-4c82-bfc3-90d5df238a8e)
### Post page
![post-page](https://github.com/dlaing240/blog-website/assets/159714200/1688994a-e1e2-4e22-adcd-e0c7dd4b4cc5)
### Comments
![comments](https://github.com/dlaing240/blog-website/assets/159714200/34d579f1-731c-4ea7-bfae-61956ab643b1)
### Login page
![login](https://github.com/dlaing240/blog-website/assets/159714200/acbba394-3724-49c1-bbf6-4cafd3798316)



