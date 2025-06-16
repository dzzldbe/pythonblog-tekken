import re

from combo import Combo

list_to = []
# generated_list = "/static/assets/df.png,/static/assets/2.png,/static/assets/next.png,/static/assets/f.png,/static/assets/1.png"
generated_list = "/static/assets/b.png,/static/assets/3.png,/static/assets/2.png,/static/assets/dhold.png,/static/assets/next.png,/static/assets/GMH.png,/static/assets/f.png,/static/assets/1.png"
cleaned_list = generated_list.split(",")
final_list = []
for i in cleaned_list:
    # a, b = i.split(".")
    i = i.removesuffix(".png")
    i = i.removeprefix("/static/assets/")
    if i.endswith("hold"):
        i = i.removesuffix("hold")
        i = i.upper()
    final_list.append(i)
# for item in final_list:
#     if item.endswith("hold"):
#         item = item.removesuffix("hold")

print(type(final_list))
print(Combo.reverse_parse(final_list))
