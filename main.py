from datetime import date
from urllib.parse import quote

from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Text
# from functools import wraps
# from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm

from extensions import db
from models.blog_post import BlogPost
from queries.blog_post_queries import BlogPostQueries

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login


# CREATE DATABASE
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = quote("ashwath@MVN123")
DB_HOST = "localhost"

SQLALCHEMY_DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DB_URI
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

blog_post = BlogPost()
blog_post_queries = BlogPostQueries()


# CONFIGURE TABLES



# TODO: Create a User table for all your registered users. 




# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register')
def register():
    return render_template("register.html")


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/logout')
def logout():
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = blog_post_queries.get_all_posts()

    if result.state != "error":
        all_posts = result.data
        return render_template("index.html", all_posts=all_posts), result.code

    return render_template("error.html", error=result.message, code=result.code), result.code


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>")
def show_post(post_id):
    result = blog_post_queries.get_post_by_id(post_id)

    if result.state == "success":
        requested_post = result.data[0]
        return render_template("post.html", post=requested_post), result.code

    return render_template("error.html", error=result.message, code=result.code), result.code


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            # author=current_user,
            author="Ashwath",
            date=date.today().strftime("%B %d, %Y")
        )

        result = blog_post_queries.add_new_post(new_post)

        if result.state == "success":
            return redirect(url_for("get_all_posts")), result.code
        else:
            return render_template("error.html", error=result.message, code=result.code), result.code
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    print(f"inside edit_post post_id ====> {post_id}")
    res = blog_post_queries.get_post_by_id(post_id)
    requested_post = res.data[0]

    edit_form = CreatePostForm(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        img_url=requested_post.img_url,
        body=requested_post.body,
    )

    if request.method == "POST":
        requested_post_id = requested_post.id
        print(f"inside edit_post requested_post id ====> {id}")
        if edit_form.validate_on_submit():
            edited_post = BlogPost(
                title=edit_form.title.data,
                subtitle=edit_form.subtitle.data,
                author="Ashwath",
                img_url=edit_form.img_url.data,
                body=edit_form.body.data,
                date=requested_post.date,
            )

            print(f"edited_post ====> {edited_post}")

            result = blog_post_queries.update_post(edited_post, requested_post)

            if result.state == "success":
                return redirect(url_for("show_post", post_id=requested_post_id)), result.code
            else:
                return render_template("error.html", error=result.message, code=result.code), result.code

    return render_template("make-post.html", add_post_form=edit_form, post_id=post_id)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    result = blog_post_queries.delete_post(post_id)

    if result.state == "success":
        return redirect(url_for('get_all_posts')), result.code
    else:
        return render_template("error.html", error=result.message, code=result.code), result.code


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    print("==================> creating tables")

    with app.app_context():
        db.create_all()

    print("==================> finished creating tables")
    app.run(debug=True, port=5002)
