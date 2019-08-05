from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post


@app.route("/")
@app.route("/index")
@login_required
def index():
    # Fake post
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Atlanta!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]

    return render_template("index.html", title="Home", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        # flask_login's @login_required decorator will make going to the index
        # page redirect here with an additional ?next=/index at the end of the
        # GET request, so we will be able to redirect to the page they were
        # trying to access after redirecting them to the login. Using
        # url_parse() keeps us safe from an attacker directing us to a
        # malicious page
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

