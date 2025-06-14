import csv
import re
from pathlib import Path

from combo import Combo

combo = "df+2 3,DF SNK 2, df+4,1,DF SNK df+1,2 T! db+2,DF SNK 3"
print(Combo.combo_parse(combo))
