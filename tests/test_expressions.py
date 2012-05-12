def test_simple(mio):
    v = mio.eval("1 + 2")
    assert v == 3


def test_complex(mio):
    v = mio.eval("1 + 2 * 3")
    assert v == 9


def test_grouping(mio):
    v = mio.eval("1 + (2 * 3)")
    assert v == 7


def test_assignment(mio):
    mio.eval("x = 1")
    v = mio.eval("x")
    assert v == 1


def test_complex_assignment1(mio):
    mio.eval("x = 1")
    v = mio.eval("x")
    assert v == 1

    mio.eval("x = x + 1")
    v = mio.eval("x")
    assert v == 2


def test_complex_assignment2(mio):
    mio.eval("Foo = Object clone")

    mio.eval("Foo x = 1")
    v = mio.eval("Foo x")
    assert v == 1

    mio.eval("Foo x = Foo x + 1")
    v = mio.eval("x")
    assert v == 2
