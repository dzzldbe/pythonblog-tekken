from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from pythonblog import db
from pythonblog.main.combo import Combo
from pythonblog.main.forms import ComboForm
from pythonblog.models import Post
from pythonblog.posts.forms import PostForm

main = Blueprint("main", __name__)


# @main.route("/")
# @main.route("/home")
# def home():
#     page = request.args.get("page", default=1, type=int)
#     posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)

#     # sorted_posts= sorted(posts.items)
#     return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/")
@main.route("/home", methods=["GET", "POST"])
def home():
    Combo.clean_folder()
    char_moves = Combo.open_scv()
    form = ComboForm(request.form)
    form1 = PostForm(request.form)
    list_assets = Combo.get_assets()
    preview_list = []
    if request.method == "POST":
        action = request.form.get("action")
        if action == "new_post":
            try:
                string1 = form.combo_string.data
                print(string1)
                form1.content.data = string1
                form1.title.data = "new test"
                # if form1.validate_on_submit():
                post = Post(
                    title=form1.title.data,
                    content=form1.content.data,
                    author=current_user,
                )
                db.session.add(post)
                db.session.commit()
                flash(message="Posted!", category="success")

                return redirect(url_for("main.home"))
            except Exception as e:
                flash(message=f"Error{e}", category="danger")
        elif action == "get_list":
            try:
                generated_list = request.form.get("generated_list")
                cleaned_list = generated_list.split(",")
                final_list = []
                for i in cleaned_list:
                    # a, b = i.split(".")
                    i = i.removesuffix(".png")
                    i = i.removeprefix("/static/assets/")
                    final_list.append(i)
                form.combo_string.data = Combo.reverse_parse(final_list)
                images = []
            except Exception as e:
                flash(message=f"Error{e}", category="danger")

        else:
            combo_string = form.combo_string.data
            combo_parsed_results = Combo.combo_parse(combo_string)
            try:
                Combo.make_image(combo_parsed=combo_parsed_results, combo_name="Asuka")
            except Exception as e:
                flash(message=f"There was and error: '{e}'", category="danger")
                # print(e)
            preview_list = Combo.make_preview(combo_parsed_results)
            images = []
            for item in preview_list:
                images.append(item)
            # return redirect(url_for("main.home_2"))

    elif request.method == "GET":
        preview_list = []
        images = []
        for item in preview_list:
            images.append(item)

    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(
        "home.html",
        title="Home",
        posts=posts,
        form=form,
        form1=form1,
        images=images,
        list_assets=list_assets,
        char_moves=char_moves,
    )
