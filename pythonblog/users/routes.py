from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from pythonblog import bcrypt, db
from pythonblog.models import Post, User
from pythonblog.users.forms import (
    LoginForm,
    RegistrationForm,
    RequestResetForm,
    ResetPasswordForm,
    UpdateAccount,
)
from pythonblog.users.functions import save_picture, send_email

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(message="Your accout has been created!", category="success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            # flash(f"Welcome {user.username} !", category="success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            hexed_picture = save_picture(form.picture.data)
            current_user.image_file = hexed_picture
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(message="Your accout has been updated!", category="success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")

    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", default=1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )

    # sorted_posts= sorted(posts.items)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("Email has been sent to you with instructions", "info")
        return redirect(url_for("users.login"))
    return render_template("request_reset.html", title="Reset Password", form=form)


@users.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is invalid password or expired token", "warning")
        return redirect(url_for("users.request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(message="Your password has been updated!", category="success")
        return redirect(url_for("users.login"))

    return render_template("reset_password.html", title="Reset Password", form=form)
