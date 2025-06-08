from flask import Blueprint, redirect, render_template, request, url_for

from pythonblog.main.combo import Combo
from pythonblog.main.forms import ComboForm
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


@main.route("/home2", methods=["GET", "POST"])
def home_2():
    form = ComboForm()
    list_assets = Combo.get_assets()
    preview_list = ["d", "df", "f", "2"]
    if request.method == "POST":
        combo_string = form.combo_string.data
        combo_parsed_results = Combo.combo_parse(combo_string)
        # Combo.make_image(combo_parsed=combo_parsed_results, combo_name="Asuka")
        preview_list = Combo.make_preview(combo_parsed_results)
        images = []
        for item in preview_list:
            images.append(item)
        # return redirect(url_for("main.home_2"))

    elif request.method == "GET":
        preview_list = [
            "assets/d.png",
            "assets/df.png",
            "assets/f.png",
            "assets/2.png",
        ]
        images = []
        for item in preview_list:
            images.append(item)

    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(
        "home_2.html",
        title="Home",
        posts=posts,
        form=form,
        images=images,
        list_assets=list_assets,
    )
