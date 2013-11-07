def test_simple(mio):
    assert mio.eval("1 + 2") == 3


def test_complex(mio):
    assert mio.eval("1 + 2 * 3") == 9


def test_grouping(mio):
    assert mio.eval("1 + (2 * 3)") == 7


def test_assignment(mio):
    mio.eval("x = 1")
    assert mio.eval("x") == 1


def test_complex_assignment_expression(mio):
    mio.eval("x = 1")
    assert mio.eval("x") == 1

    mio.eval("x = x + 1")
    assert mio.eval("x") == 2


def test_complex_assignment_attribute(mio):
    mio.eval("Foo = Object clone()")

    mio.eval("Foo x = 1")
    assert mio.eval("Foo x") == 1

    mio.eval("Foo x = Foo x + 1")
    assert mio.eval("Foo x") == 2
