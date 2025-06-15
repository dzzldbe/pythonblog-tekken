import csv
import re
from pathlib import Path

from combo import Combo

combo = "df+2 3,DF SNK 2, df+4,1,DF SNK df+1,2 T! db+2,DF SNK 3"

# combo = "DF SNK 3,"
ste = ""
char_moves = []
stance_check = []
p = Path.cwd() / "pythonblog/static/char_assets/char_assets.csv"
with open(p) as file:
    reader = csv.reader(file, delimiter=";")
    for line in reader:
        char, moves = line
        character = {"char": char, "moves": moves}
        char_moves.append(character)
for cm in char_moves:
    moves = cm["moves"].split(",")
    for move in moves:
        move = move.strip()
        stance_check.append(move)
        ste += str(move + "|")
special_stance = rf"(?:{ste})"
special_stance = special_stance[:-2] + ")"
# print(special_stance)

stance = r"(?:SSL|SSR|FC|WS|WR|SS|BT)"
# special_stance = rf"(?:{s_s})"
motion = (
    r"(?:dash|DASH|Dash|qcf|qcb|hcf|hcb|uf|ub|db|df|CH|f|F|b|B|u|U|d|D|DF|DB|UB|UF|n)"
)
button_input = r"(?:(?:\+|~)?[1-4](?:(?:\+|~)[1-4])*)"

pattern = re.compile(
    rf"^(T!|{special_stance}|{stance}|(?:{motion})?|{motion}{button_input}|({button_input}[~]{motion})|{button_input}|{button_input}*)$"
)
combo_input = combo.strip()
raw_parts = re.split(r"[/s/.]", combo_input)
# parsed list of individual attacks
results = []
for part in raw_parts:
    if part in stance_check:
        part += ","
        results.append(part)
    elif pattern.fullmatch(part):
        results.append(part)
        results.append("next")
    elif "," in part:
        list_coma = part.split(",")
        for _ in list_coma:
            if pattern.fullmatch(_):
                results.append(_)
        results.append("next")
print(stance_check)
# print(combo)
# print("---")
# print(raw_parts)
# print("---")
# print(results)
# results.pop()
# return results
