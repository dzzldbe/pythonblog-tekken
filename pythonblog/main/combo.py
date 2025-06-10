import os
import re
import secrets
import time
from pathlib import Path

from flask import current_app
from PIL import Image


class Combo:
    def __init__(self, name, input):
        self.name = name
        self.input = input

    def combo_parse(combo):
        stance = r"(?:SSL|SSR|FC|WS|WR|SS|BT)"
        special_stance = r"(?:GMH)"
        motion = r"(?:dash|DASH|Dash|qcf|qcb|hcf|hcb|uf|ub|db|df|CH|f|F|b|B|u|U|d|D|n)"
        button_input = r"(?:(?:\+|~)?[1-4](?:(?:\+|~)[1-4])*)"

        pattern = re.compile(
            rf"^(T!|{special_stance}|{stance}|(?:{motion})?|{motion}{button_input}|({button_input}[~]{motion})|{button_input}|{button_input}*)$"
        )
        combo_input = combo.strip()
        raw_parts = re.split(r"[\s\.]+", combo_input)
        # parsed list of individual attacks
        results = []
        for part in raw_parts:
            if pattern.fullmatch(part):
                results.append(part)
                results.append("next")
            elif "," in part:
                list_coma = part.split(",")
                for _ in list_coma:
                    if pattern.fullmatch(_):
                        results.append(_)
                results.append("next")
        results.pop()
        return results

    def make_preview(combo_parsed):
        ind_input = []
        final_list = []
        # path_assets = Path.cwd() / "pythonblog/static/assets"

        list_assets = (
            "1+2",
            "1+3",
            "1+4",
            "2+3",
            "2+4",
            "3+4",
            "f",
            "F",
            "dash",
            "qcf",
            "hcf",
            "hcb",
            "ub",
            "db",
            "uf",
            "df",
            "CH",
            "b",
            "B",
            "u",
            "U",
            "d",
            "D",
            "n",
            "1",
            "2",
            "3",
            "4",
            "~",
            "T!",
            "next",
        )
        char_stance = "GMH"
        list_stance = [
            "FC",
            "SSL",
            "SSR",
            "WS",
            "WR",
            "wr",
            "SS",
            "BT",
            f"{char_stance}",
        ]
        for res in combo_parsed:
            if res in list_assets:
                ind_input.append(res)
            elif res in list_stance:
                ind_input.append(res)
            elif "+" in res:
                res_splits = res.split(sep="+", maxsplit=1)
                for _ in res_splits:
                    ind_input.append(_)
            elif "~" in res:
                a, b = res.split(sep="~", maxsplit=1)
                ind_input.append(a)
                ind_input.append("~")
                ind_input.append(b)

        for _ in ind_input:
            if _ == "F":
                final_list.append("assets/fhold.png")
            elif _ == "D":
                final_list.append("assets/dhold.png")
            elif _ == "U":
                final_list.append("assets/uhold.png")
            elif _ == "B":
                final_list.append("assets/bhold.png")
            elif _ == "DB":
                final_list.append("assets/dbhold.png")
            elif _ == "DF":
                final_list.append("assets/dfhold.png")
            elif _ == "UB":
                final_list.append("assets/ubhold.png")
            elif _ == "UF":
                final_list.append("assets/ufhold.png")
            elif _ == "qcf":
                final_list.append("assets/d.png")
                final_list.append("assets/df.png")
                final_list.append("assets/f.png")
            elif _ == "qcb":
                final_list.append("assets/d.png")
                final_list.append("assets/db.png")
                final_list.append("assets/b.png")
            else:
                final_list.append(f"assets/{_}.png")

        return final_list

    def make_image(combo_parsed, combo_name):
        images = []
        ind_input = []
        random_hex = secrets.token_hex(8)
        file_name = combo_name + random_hex + ".png"
        file_path = os.path.join(
            current_app.root_path, f"static/combo_pics/{file_name}"
        )
        path_assets = Path.cwd() / "pythonblog/static/assets"
        # combo_path = Path.cwd() / f"{combo_name}.png"
        list_assets = (
            "1+2",
            "1+3",
            "1+4",
            "2+3",
            "2+4",
            "3+4",
            "f",
            "F",
            "dash",
            "qcf",
            "hcf",
            "hcb",
            "ub",
            "db",
            "uf",
            "df",
            "CH",
            "b",
            "B",
            "u",
            "U",
            "d",
            "D",
            "n",
            "1",
            "2",
            "3",
            "4",
            "~",
            "T!",
            "next",
        )
        char_stance = "GMH"
        list_stance = [
            "FC",
            "SSL",
            "SSR",
            "WS",
            "WR",
            "wr",
            "SS",
            "BT",
            f"{char_stance}",
        ]

        for res in combo_parsed:
            if res in list_assets:
                ind_input.append(res)
            elif res in list_stance:
                ind_input.append(res)
            elif "+" in res:
                res_splits = res.split(sep="+", maxsplit=1)
                for _ in res_splits:
                    ind_input.append(_)
            elif "~" in res:
                a, b = res.split(sep="~", maxsplit=1)
                ind_input.append(a)
                ind_input.append("~")
                ind_input.append(b)
        # ind_input.pop(0)
        for _ in ind_input:
            if _ == "F":
                images.append(Image.open(f"{path_assets}/fhold.png"))
            elif _ == "qcf":
                images.append(Image.open(f"{path_assets}/d.png"))
                images.append(Image.open(f"{path_assets}/df.png"))
                images.append(Image.open(f"{path_assets}/f.png"))
            else:
                images.append(Image.open(f"{path_assets}/{_}.png"))

        total_height = max(img.width for img in images)

        total_width = sum(img.width for img in images)
        new_img = Image.new(
            "RGBA", (total_width, total_height), color=(116, 148, 173, 255)
        )

        x_offset = 0

        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width
        final_image = new_img.convert("RGB")

        final_image.save(file_path)

    def get_assets():
        assets = []
        path = Path("pythonblog/static/assets")
        for p in path.iterdir():
            p1 = "assets/" + p.name
            assets.append(p1)
        return assets

    def clean_folder():
        p = Path.cwd() / "pythonblog/static/combo_pics"
        # time.sleep(10)
        for f in p.glob("*"):
            try:
                f.unlink()
            except Exception as e:
                pass

    def reverse_parse(form_list):
        form_string = "Combo: "
        for i, move in enumerate(form_list):
            if i + 1 < len(form_list):
                next_move = form_list[i + 1]
                if move == "next":
                    form_string += " "
                elif (
                    re.match("^[a-zA-Z]*$", move)
                    and re.match("^[1-4]*$", next_move)
                    and move != "next"
                ):
                    form_string += move + "+"
                elif re.match("[1-4]*", move) and re.match("[1-4]*", next_move):
                    form_string += move + ","

                else:
                    form_string += move
        form_string += form_list[-1]
        return form_string
