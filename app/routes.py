from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    # Fake user
    user = {"username": "Gregory"}
    # Fake post
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Atlanta!"
        },
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!"
        }
    ]
            
    return render_template("index.html", title="Home", user=user, posts=posts)
