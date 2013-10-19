#from pytest import raises

#from mio import runtime
#from mio.errors import AttributeError, TypeError


def test_parens(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("(x)") == 1


def test_ifNone(mio):
    assert mio.eval("x = None").value is None
    assert mio.eval("x ifNone(1)") == 1

    assert mio.eval("x = 1") == 1
    assert mio.eval("x ifNone(2)") == 1


def test_ifTrue(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("""(x == 1) ifTrue("foo")""") == "foo"
    assert mio.eval("""(x != 1) ifTrue("foo")""").value is False


def test_ifFalse(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("""(x != 1) ifFalse("foo")""") == "foo"
    assert mio.eval("""(x == 1) ifFalse("foo")""").value is True


def test_ifTrue_ifFalse(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("""(x == 1) ifTrue("foo") ifFalse("bar")""") == "foo"

    assert mio.eval("x = 1") == 1
    assert mio.eval("""(x != 1) ifTrue("foo") ifFalse("bar")""") == "bar"


def test_or(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("x or False") == 1


def test_and(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("x and \"foo\"") == "foo"


def test_or_and(mio):
    assert mio.eval("x = 1") == 1
    assert mio.eval("y = 0") == 0
    assert mio.eval("x or y and \"foo\"").value is True
    assert mio.eval("(x or y) and \"foo\"") == "foo"
    assert mio.eval("x or (y and \"foo\")") == 1
