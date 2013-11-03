from operator import attrgetter


from mio.lexer import tokenize


def test1():
    tokens = tokenize("1 + 2")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "1 + 2"


def test2():
    tokens = tokenize("1 + 2 * 3")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "1 + ( 2 * 3 )"


def test3():
    tokens = tokenize("1 + 2 * 3 + 4")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "1 + ( 2 * 3 ) + 4"


def test4():
    tokens = tokenize("x = x + 1")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "x = x + 1"


def test5():
    tokens = tokenize("x = x + 1 + 2")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "x = x + 1 + 2"


def test6():
    tokens = tokenize("x = x + 1 + 2 * 3")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "x = x + 1 + ( 2 * 3 )"


def test7():
    tokens = tokenize("1 + ( 2 * 3 )")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "1 + ( 2 * 3 )"


def test8():
    tokens = tokenize("( 1 + 2 ) * 3")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "( 1 + 2 ) * 3"


def test9():
    tokens = tokenize("x = 1 + 2 * 3 ; y = 4")
    output = " ".join(map(attrgetter("value"), tokens))
    assert output == "x = 1 + ( 2 * 3 ) ; y = 4"
