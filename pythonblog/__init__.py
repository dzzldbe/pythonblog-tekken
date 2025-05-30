from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from pythonblog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# app.config.from_pyfile

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
