import random
import string
from pathlib import Path

from combo import Combo
from flask import url_for


# path = Path.cwd() / "pythonblog/assets"
# for p in path.glob("*.png", case_sensitive=None):
#     print(p)
# print(path)
# for p in Path().iterdir():
#     print(p)
# def get_assets():
#     assets = []
#     path = Path("pythonblog/static/assets")
#     for p in path.iterdir():
#         assets.append(p.name)
#     return assets
def clean_folder():
    p = Path.cwd() / "pythonblog/static/combo_pics"
    print(p)
    for f in p.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass


clean_folder()
# clean_folder()
# print(pythonblog.name)
