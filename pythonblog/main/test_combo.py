from pythonblog.main.combo import Combo

combo1 = "df+2 3,DF SNK 2, df+4,1,DF SNK df+1,2 T! db+2,DF SNK 3"


def test_combo_parse():
    assert Combo.combo_parse(combo1) == [
        "df+2",
        "next",
        "3,DF",
        "next",
        "SNK 2",
        "next",
        "df+4,1,DF",
        "next",
        "SNK df+1,2",
        "next",
        "T!",
        "next",
        "db+2,DF",
        "next",
        "SNK 3",
    ]
