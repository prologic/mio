from mio.core.message import Message


def test_name(mio):
    m = Message("foo")
    assert m.name == "foo"


def test_args(mio):
    args = [Message("%d" % i) for i in range(3)]
    m = Message("foo", args=args)
    assert m.name == "foo"
    assert m.args[0].name == "0"
    assert m.args[1].name == "1"
    assert m.args[2].name == "2"


def test_next_previous(mio):
    m = Message("foo")
    m.next = Message("bar")

    assert m.previous is m
    assert m.name == "foo"
    assert m.next.name == "bar"
    assert m.next.next is None
    assert m.next.previous.name == "foo"


def test_setName(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setName(\"foo\")")
    assert m.name == "foo"


def test_setValue(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setValue(\"foo\")")
    assert m.value == "foo"


def test_setArgs(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]


def test_getArgs(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]
    assert list(mio.eval("m args")) == [1, 2, 3]


def test_evalArg(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]
    assert mio.eval("m arg(0)") == 1
    assert mio.eval("m arg(1)") == 2
    assert mio.eval("m arg(2)") == 3
    assert mio.eval("m arg(3)").value is None


def test_evalArgs(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("m setArgs(1, 2, 3)")
    assert m.args == [1, 2, 3]
    assert list(mio.eval("m evalArgs()")) == [1, 2, 3]


def test_getFirst(mio):
    m = mio.eval("m = Message clone()")
    mio.eval("n = Message clone()")
    mio.eval("m setNext(n)")
    assert mio.eval("m first") is m
    assert mio.eval("n first") is m


def test_getNext(mio):
    mio.eval("m = Message clone()")
    n = mio.eval("n = Message clone()")
    mio.eval("m setNext(n)")
    assert mio.eval("m next") is n
    assert mio.eval("n next") is None


def test_getLast(mio):
    mio.eval("m = Message clone()")
    mio.eval("n = Message clone()")
    o = mio.eval("o = Message clone()")
    mio.eval("m setNext(n)")
    mio.eval("n setNext(o)")
    assert mio.eval("m last") is o
    assert mio.eval("n last") is o
    assert mio.eval("o last") is o


#XXX: Broken
#def test_eval(mio, capfd):
#    mio.eval("m = Message clone() setName(\"print\") setArgs(Message clone() setName(\"foo\") setValue(\"foo\"))")
#    assert mio.eval("m eval()").value is None
#    out, err = capfd.readouterr()
#    assert out == "foo\n"


def test_call(mio):
    mio.eval("Foo = Object clone()")
    mio.eval("""Foo __call__ = method("foo")""")
    assert mio.eval("Foo()") == "foo"


def test_get(mio):
    mio.eval("Foo = Object clone()")
    mio.eval("Bar = Object clone()")
    mio.eval("""Bar __get__ = method(obj, "bar")""")
    mio.eval("Foo bar = Bar")
    assert mio.eval("Foo bar") == "bar"


def test_state_stop(mio, capfd):
    mio.eval("""foo = block(x = 1; print(x); state setReturn(2); print("foo"))""")
    assert mio.eval("foo()") == 2
    out, err = capfd.readouterr()
    assert out == "1\n"
