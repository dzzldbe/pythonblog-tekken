from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from pythonblog import db
from pythonblog.models import Post
from pythonblog.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/new_post", methods=["GET", "POST"])
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
        redirect(url_for("main.home"))
    return render_template(
        "new_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(ident=id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("posts.post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "new_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/<int:id>/delete_post", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(message="Your Post has been deleted!", category="success")
    return redirect(url_for("main.home"))
