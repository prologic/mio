from pytest import raises


from mio import runtime
from mio.errors import AttributeError, TypeError


def test_clone(mio):
    mio.eval("World = Object clone()")
    assert mio.eval("World")
    assert mio.eval("World parent") == runtime.find("Object")


def test_type(mio):
    assert mio.eval("Object type") == "Object"
    assert mio.eval("1 type") == "Number"


def test_setParent(mio):
    assert mio.eval("World = Object clone()")
    assert mio.eval("World parent") == runtime.find("Object")

    with raises(TypeError):
        mio.eval("World setParent(World)", reraise=True)

    assert mio.eval("Foo = Object clone()")
    assert mio.eval("World setParent(Foo)")
    assert mio.eval("World parent") == mio.eval("Foo")


def test_do(mio):
    mio.eval("do(x = 1)")
    assert mio.eval("x") == 1


def test_eq(mio):
    assert mio.eval("1 ==(1)")


def test_forward(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo x") == 1
    assert mio.eval("Foo Object") == runtime.find("Object")


def test_get(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1

    with raises(AttributeError):
        mio.eval("Foo z", reraise=True)


def test_get_no_forward(mio):
    mio.eval("Foo = Object clone()")
    mio.eval("Foo del(\"forward\")")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1

    with raises(AttributeError):
        mio.eval("Foo z", reraise=True)


def test_has(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo has(\"x\")")


def test_has2(mio):
    mio.eval("Foo = Object clone()")
    assert not mio.eval("Foo has(\"x\")")


def test_hash(mio):
    assert mio.eval("Object __hash__()") == hash(runtime.find("Object"))


def test_id(mio):
    assert mio.eval("(Object id) == (Object id)")


def test_keys(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo y = 2")
    keys = list(mio.eval("Foo keys"))
    assert "x" in keys
    assert "y" in keys


def test_method(mio):
    mio.eval("foo = method(1)")
    assert mio.eval("foo()") == 1

    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1") == 1

    mio.eval("Foo foo = method(self x)")
    assert mio.eval("Foo foo()") == 1


def test_neq(mio):
    assert mio.eval("1 !=(0)")


def test_set(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1
    assert mio.eval("Foo set(\"x\", 2)") == 2
    assert mio.eval("Foo x") == 2


def test_del(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo count = 1")
    assert mio.eval("Foo del(\"count\")").value is None

    with raises(AttributeError):
        mio.eval("Foo count", reraise=True)


def test_print(mio, capfd):
    assert mio.eval("print(\"Hello World!\")").value is None
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"


def test_print_sep(mio, capfd):
    assert mio.eval("print(1, 2, 3, sep=\", \")").value is None
    out, err = capfd.readouterr()
    assert out == "1, 2, 3\n"


def test_print_end(mio, capfd):
    assert mio.eval("print(1, 2, 3, end=\"\")").value is None
    out, err = capfd.readouterr()
    assert out == "1 2 3"


def test_repr(mio):
    assert mio.eval("1 __repr__()") == "1"
    assert mio.eval("\"foo\"__repr__()") == "u\"foo\""


def test_str(mio):
    assert mio.eval("1 __str__()") == "1"
    assert mio.eval("\"foo\" __str__()") == "foo"


def test_bool(mio):
    assert mio.eval("bool(1)")
    assert not mio.eval("bool(0)")
    assert mio.eval("bool(\"foo\")")
    assert not mio.eval("bool(\"\")")


def test_parent(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo parent is Object")


def test_parent2(mio):
    assert mio.eval("Object parent is Object")


def test_value(mio):
    assert mio.eval("Object value is None")


def test_setValue(mio):
    mio.eval("Foo = Object clone()")
    assert mio.eval("Foo value is None")

    mio.eval("Foo setValue(1)")
    assert mio.eval("Foo value == 1")


def test_primitive(mio):
    mio.eval("Foo = Object :clone()")
    assert not mio.eval("Foo is Object")


def test_primitive2(mio):
    with raises(AttributeError):
        mio.eval("Object :asdf", reraise=True)


def test_state(mio):
    assert repr(mio.eval("state")) == "NormalState()"
