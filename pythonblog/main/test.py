import random
import string
from pathlib import Path
from flask import url_for
from combo import Combo


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return "".join(random.choice(characters) for _ in range(length))


random_string = generate_random_string(12)
# path_assets = Path.cwd() / "pythonblog/static/assets"
combo_1 = Combo(
    name="jack",
    input=Combo.combo_parse("f,F+2,F df+2 df+1 f+2,3,F df+1,F~2 T! uf+3+4,1+2"),
)
Combo.make_image(combo_parsed=combo_1.input, combo_name=random_string)



 <!-- <input class="form-control form-control-lg"
                               type="text"
                               placeholder="Input your combo:"
                               style="border:5px;
                                      text-align: end;
                                      color: chocolate"> -->
# print(path_assets)

@main.route("/home2", methods=["GET", "POST"])
def home_2():
    form = ComboForm()
    if request.method == "POST":
        combo_string = form.combo_string.data
        combo_parsed_results = Combo.combo_parse(combo_string)
        Combo.make_image(combo_parsed=combo_parsed_results, combo_name="Asuka")

        return redirect(url_for("main.home_2"))

    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home_2.html", title="Home", posts=posts, form=form)

url_for()