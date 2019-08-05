from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# This forces unlogged users to to login page if they try to view a page that
# we only want logged in users to see. We specificy these pages with the
# @login_required decorated imported from flask_login
login.login_view = "login"

from app import routes, models
