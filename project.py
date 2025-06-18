import csv
import re
from pathlib import Path


def main():
    def open_scv():
        char_moves = []
        p = (
            Path(__file__).resolve().parent
            / "pythonblog/static/char_assets/char_assets.csv"
        )
        with open(p) as file:
            reader = csv.reader(file, delimiter=";")
            for line in reader:
                char, moves = line
                character = {"char": char, "moves": moves}
                char_moves.append(character)
        return char_moves

    #     print(open_scv())

    def combo_parse(combo):
        ste = ""
        char_moves = []
        stance_check = []
        p = (
            Path(__file__).resolve().parent
            / "pythonblog/static/char_assets/char_assets.csv"
        )
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
                stance_check.append(move)
                ste += str(move + ".|")
        special_stance = rf"(?:{ste})"
        special_stance = special_stance[:-2] + ")"
        # print(special_stance)

        stance = r"(?:SSL|SSR|FC|WS|WR|SS|BT)"
        # special_stance = rf"(?:{s_s})"
        motion = r"(?:dash|DASH|Dash|qcf|qcb|hcf|hcb|uf|ub|db|df|CH|f|F|b|B|u|U|d|D|DF|DB|UB|UF|n)"
        button_input = r"(?:(?:\+|~)?[1-4](?:(?:\+|~)[1-4])*)"

        pattern = re.compile(
            rf"^(T!|{special_stance}|{stance}|(?:{motion})?|{motion}{button_input}|({button_input}[~]{motion})|{button_input}|{button_input}*)$"
        )
        combo_input = combo.strip()
        raw_parts = re.split(r"[\s\.]+", combo_input)
        # parsed list of individual attacks
        results = []
        for part in raw_parts:
            if part in stance_check:
                # part += ","
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
        results.pop()
        return results

    print(combo_parse())


#     print(Path(__file__).resolve().parent)


if __name__ == "__main__":
    main()
