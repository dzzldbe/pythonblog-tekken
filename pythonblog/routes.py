import os
import secrets

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image

from pythonblog import app, bcrypt, db, mail
from pythonblog.forms import (
    LoginForm,
    PostForm,
    RegistrationForm,
    RequestResetForm,
    ResetPasswordForm,
    UpdateAccount,
)
from pythonblog.models import Post, User


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    # sorted_posts= sorted(posts.items)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            # flash(f"Welcome {user.username} !", category="success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    file_name = random_hex + file_ext
    file_path = os.path.join(app.root_path, f"static/profile_pics/{file_name}")
    output_size = (125, 125)
    with Image.open(form_picture) as img:
        img.thumbnail(output_size)
        # ImageOps.contain(img, output_size)
        img.save(file_path)
    # form_picture.save(file_path)

    return file_name


@app.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")

    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash(message="Posted!", category="success")
        redirect(url_for("home"))
    return render_template(
        "new_post.html", title="New Post", form=form, legend="New Post"
    )


@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(ident=id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    form = PostForm()
    post = Post.query.get_or_404(ident=id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "new_post.html", title="Update Post", form=form, legend="Update Post"
    )


@app.route("/<int:id>/delete_post", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(message="Your Post has been deleted!", category="success")
    return redirect(url_for("home"))


@app.route("/user/<string:username>")
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


def send_email(user):
    token = User.get_reset_token(user)
    msg = Message(
        subject="Password Reset Request",
        recipients=[user.email],
        sender=os.environ.get("MY_GMAIL"),
    )
    msg.body = f"To reset your password, visit the following link: \
        {url_for('reset_password', token=token, _external=True)}\
            If you did not make this requset, please ignore it."
    mail.send(msg)


@app.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("Email has been to you with instructions", "warning")
        return redirect(url_for("login"))
    return render_template("request_reset.html", title="Reset Password", form=form)


@app.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is invalid password or expired token", "warning")
        return redirect(url_for("request_reset"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(message="Your password has been updated!", category="success")
        return redirect(url_for("login"))

    return render_template("reset_password.html", title="Reset Password", form=form)
