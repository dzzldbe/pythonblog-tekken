import csv
from pathlib import Path

ste = ""
char_moves = []
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
        move.strip()
        ste += str(move + "|")
special_stance = rf"(?:{ste})"

special_stance = special_stance[:-2] + ")"


# print("----")
print(special_stance)
