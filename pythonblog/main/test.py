import csv
import re
from pathlib import Path

import pytest
from combo import Combo

# correct_combo1=[]
# combo_list=[]
# path_to_file = Path.home() / "Desktop/my_project/pythonblog/static/combos_list.csv"
# with open(path_to_file) as file:
#     reader = csv.DictReader(file, delimiter=";")
#     for row in reader:
#         combo_list.append({"char": row["Char"], "combos": row["Combos"]})


# for char in combo_list:
#     combo_1, combo_2 = char["combos"].split("$")
#     # print(f"{char['char']}'s combo #1 is: {combo_1}")
#     correct_combo = combo_1.split(" ")
#     for item in correct_combo:
#         correct_combo1.append(item)
#         correct_combo1.append("next")
def test_parse():
    correct_combo1 = []
    combo_list = []
    path_to_file = Path.home() / "Desktop/my_project/pythonblog/static/combos_list.csv"
    with open(path_to_file) as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            combo_list.append({"char": row["Char"], "combos": row["Combos"]})

    for char in combo_list:
        combo_1, combo_2 = char["combos"].split("$")
        # print(f"{char['char']}'s combo #1 is: {combo_1}")
        correct_combo = combo_1.split(" ")
        for item in correct_combo:
            correct_combo1.append(item)
            correct_combo1.append("next")
        # assert Combo.combo_parse(correct_combo) == correct_combo1
        correct_combo1.clear()


test_parse()
