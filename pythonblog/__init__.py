import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_APP")
app.config["MAIL_USERNAME"] = os.environ.get("MY_GMAIL")


db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = "users.login"  # route page
login_manager.login_message_category = "info"


mail = Mail(app)


from pythonblog.main.routes import main
from pythonblog.posts.routes import posts
from pythonblog.users.routes import users

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
