import os

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.environ.get("SECRET_KEY")
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_PASSWORD = os.environ.get("MAIL_APP")
MAIL_USERNAME = os.environ.get("MY_GMAIL")
