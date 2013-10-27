def test_parens(mio):
    assert mio.eval("(1)") == 1


def test_ifNone(mio):
    assert mio.eval("None ifNone(1)") == 1
    assert mio.eval("1 ifNone(2)") == 1


def test_ifTrue(mio):
    assert mio.eval("""(1 == 1) ifTrue("foo")""") == "foo"
    assert not mio.eval("""(1 != 1) ifTrue("foo")""")


def test_ifFalse(mio):
    assert mio.eval("""(1 != 1) ifFalse("foo")""") == "foo"
    assert mio.eval("""(1 == 1) ifFalse("foo")""")


def test_ifTrue_ifFalse(mio):
    assert mio.eval("""(1 == 1) ifTrue("foo") ifFalse("bar")""") == "foo"
    assert mio.eval("""(1 != 1) ifTrue("foo") ifFalse("bar")""") == "bar"


def test_or(mio):
    assert mio.eval("1 or False") == 1

    assert mio.eval("True or False")
    assert mio.eval("True or True")
    assert not mio.eval("False or False")
    assert mio.eval("False or True")


def test_and(mio):
    assert mio.eval("True and \"foo\"") == "foo"

    assert not mio.eval("True and False")
    assert mio.eval("True and True")
    assert not mio.eval("False and False")
    assert not mio.eval("False and True")


def test_or_and(mio):
    assert mio.eval("1 or 0 and \"foo\"")
    assert mio.eval("(1 or 0) and \"foo\"") == "foo"
    assert mio.eval("1 or (0 and \"foo\")") == 1
