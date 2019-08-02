from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    # Fake user
    user = {"username": "Gregory"}
    # Fake post
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Atlanta!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]

    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # The template defines this post request
    
    # form.validate_on_submit() returns false for the GET on "/login", so we
    # render the login template. On POST, it will gather everything, run the
    # validators, make sure everything is ok, and return true. If there are any
    # problems it will return false and the form will be rendered back to the
    # user
    if form.validate_on_submit():
        # Flash will help us render a message on the page, but we still need to
        # put it in the template
        flash("Login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data))
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)
