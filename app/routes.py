from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
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


# This <username> syntax means that flask will accept anything here, and map
# whatever is there to the username arguemnt in the user function below
@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post 1"},
        {"author": user, "body": "Test post 2"},
    ]
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for("edit_profile"))
    # Prepopulate fields with data in database if it is a GET request
    # BUT, the above if statement could also fail if there is invalid form
    # data. In that case, we don't want to prefill and instead just return the
    # form data and it will render the errors because of how we've written it
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)



@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
