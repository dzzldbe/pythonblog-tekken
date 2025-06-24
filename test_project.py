from project import combo_parse, get_assets, open_scv


def test_open_scv():
    return_results = open_scv()
    assert isinstance(return_results, list)


def test_combo_parse():
    combo = "df+2 f+4 b+3,2 b+3,2,D GMH.f+1 T! B+2"
    assert combo_parse(combo) == [
        "df+2",
        "next",
        "f+4",
        "next",
        "b+3",
        "2",
        "next",
        "b+3",
        "2",
        "D",
        "next",
        "GMH",
        "f+1",
        "next",
        "T!",
        "next",
        "B+2",
    ]


def test_get_assets():
    return_results = get_assets()
    assert isinstance(return_results, list)
