from gflanguages import lang_support


def test_LoadLanguages():
    langs = lang_support.LoadLanguages()
    numerals = langs["yi_Hebr"].exemplar_chars.numerals
    assert numerals == '- ‑ , . % ‰ + 0 1 2 3 4 5 6 7 8 9'


def test_LoadScripts():
    scripts = lang_support.LoadScripts()
    assert scripts["Tagb"].name == 'Tagbanwa'


def test_LoadRegions():
    regions = lang_support.LoadRegions()
    br = regions["BR"]
    assert br.name == 'Brazil'
    assert br.region_group == ['Americas']
