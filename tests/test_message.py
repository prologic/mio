from mio.message import Message


def test_name(mio):
    m = Message("foo")
    assert m.name == "foo"


def test_args(mio):
    args = [Message("%d" % i) for i in range(3)]
    m = Message("foo", *args)
    assert m.name == "foo"
    assert m.args[0].name == "0"
    assert m.args[1].name == "1"
    assert m.args[2].name == "2"


def test_next_previous(mio):
    m = Message("foo")
    m.next = Message("bar")

    assert m.previous == None
    assert m.name == "foo"
    assert m.next.name == "bar"
    assert m.next.next == None
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

def test_eval(mio):
    mio.eval("m = Message clone setName(\"foo\") setValue(\"foo\")")
    mio.eval("m setNext(Message clone setName(\"println\"))")
    assert mio.eval("m eval") == "foo"
