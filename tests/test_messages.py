from mio.message import Message


def test_name():
    m = Message("foo")
    assert m.name == "foo"


def test_args():
    args = [Message("%d" % i) for i in range(3)]
    m = Message("foo", *args)
    assert m.name == "foo"
    assert m.args[0].name == "0"
    assert m.args[1].name == "1"
    assert m.args[2].name == "2"


def test_next_previous():
    m = Message("foo")
    m.next = Message("bar")

    assert m.previous is m
    assert m.name == "foo"
    assert m.next.name == "bar"
    assert m.next.next is None
    assert m.next.previous.name == "foo"


def test_setName(mio):
    m = mio.eval("m = Message clone")
    mio.eval("m setName(\"foo\")")
    assert m.name == "foo"


def test_setValue(mio):
    m = mio.eval("m = Message clone")
    mio.eval("m setValue(\"foo\")")
    assert m.value == "foo"


def test_setArgs(mio):
    m = mio.eval("m = Message clone")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]


def test_getArgs(mio):
    m = mio.eval("m = Message clone")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]
    assert list(mio.eval("m args")) == [1, 2, 3]


def test_evalArg(mio):
    m = mio.eval("m = Message clone")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]
    assert mio.eval("m arg(0)") == 1
    assert mio.eval("m arg(1)") == 2
    assert mio.eval("m arg(2)") == 3
    assert mio.eval("m arg(3)").value is None


def test_eval(mio):
    mio.eval("m = Message clone setName(\"foo\") setValue(\"foo\")")
    mio.eval("m setNext(Message clone setName(\"println\"))")
    assert mio.eval("m eval") == "foo"
