import csv
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
# char_moves = Combo.open_scv()
# print(char_moves)
# char_moves = []
# p = Path.cwd() / "pythonblog/static/char_assets/char_assets.csv"
# with open(p) as file:
#     reader = csv.reader(file, delimiter=";")
#     for line in reader:
#         char, moves = line
#         character = {"char": char, "moves": moves}
#         char_moves.append(character)
# # char_test = "Jack 8"
# for char in char_moves:
#     if char["char"] == char_test:
#         print(char["moves"])
#     else:
#         pass
test = Combo.open_scv()
for i in test:
    print(i["char"])
