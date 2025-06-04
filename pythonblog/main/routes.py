from flask import Blueprint, render_template, request

from pythonblog.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)

    # sorted_posts= sorted(posts.items)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/home2")
def home_2():
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home_2.html", title="Home", posts=posts)
