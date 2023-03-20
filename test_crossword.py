import crossword

def test_add_down():
    cw = crossword("hello")
    cw.add_down()
    assert cw.down[0][0] == 'H'

def test_add_down_2():
    cw = crossword("hello")
    cw.add_down()
    cw.add_across()
    cw.add_down()
    assert cw.down[1][0] == "E"