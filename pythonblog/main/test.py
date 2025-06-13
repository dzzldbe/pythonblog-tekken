# import csv
# import random
import re

# import string
# from pathlib import Path

# from combo import Combo
# from flask import url_for


def reverse_parse(form_list):
    form_string = "Combo: "
    i = 0
    while len(form_list) > i:
        move = form_list[i]
        if len(form_list) > i + 1:
            next_move = form_list[i + 1]
        else:
            next_move = ""
        if move == "next":
            form_string += " "
        elif move == "dhold":
            form_string += "D"
        elif move == "dbhold":
            form_string += "DB"
        elif move == "dfhold":
            form_string += "DF"
        elif move == "uhold":
            form_string += "U"
        elif move == "ubhold":
            form_string += "UB"
        elif move == "ufhold":
            form_string += "UF"
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
        # print(form_string)
        i += 1
    return form_string


cmb_list = ["dhold", "dhold", "dhold"]
print(reverse_parse(cmb_list))
