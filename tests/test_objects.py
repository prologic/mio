from pytest import raises

from mio import runtime
from mio.errors import AttributeError, TypeError


def test_clone(mio):
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World parent") == runtime.find("Object")


def test_setParent(mio):
    assert mio.eval("World = Object clone")
    assert mio.eval("World parent") == runtime.find("Object")

    with raises(TypeError):
        mio.eval("World setParent(World)", reraise=True)

    assert mio.eval("Foo = Object clone")
    assert mio.eval("World setParent(Foo)")
    assert mio.eval("World parent") == mio.eval("Foo")


def test_do(mio):
    mio.eval("do(x = 1)")
    assert mio.eval("x") == 1


def test_eq(mio):
    assert mio.eval("1 ==(1)")


def test_foreach(mio):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]

    mio.eval("""
        sum = method(iterable,
            sum = 0
            iterable foreach(item,
                sum = sum + item
            )
            sum
        )
    """)

    assert mio.eval("sum(xs)") == 6


def test_forward(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo x") == 1
    assert mio.eval("Foo Object") == runtime.find("Object")


def test_get(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1

    with raises(AttributeError):
        mio.eval("Foo z", reraise=True)


def test_has(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo has(\"x\")") == True


def test_hash(mio):
    assert mio.eval("Object hash") == hash(runtime.find("Object"))


def test_id(mio):
    assert mio.eval("Object id") == id(runtime.find("Object"))


def test_keys(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo y = 2")
    keys = list(mio.eval("Foo keys"))
    assert "x" in keys
    assert "y" in keys


def test_method(mio):
    mio.eval("foo = method(1)")
    assert mio.eval("foo") == 1

    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1") == 1

    mio.eval("Foo foo = method(self x)")
    assert mio.eval("Foo foo") == 1


def test_neq(mio):
    assert mio.eval("1 !=(0)") == True


def test_println(mio):
    pass


def test_set(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1
    assert mio.eval("Foo set(\"x\", 2)") == 2
    assert mio.eval("Foo x") == 2


def test_del(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo a = 1")
    assert mio.eval("Foo del(\"a\")") == None

    with raises(AttributeError):
        mio.eval("Foo a", reraise=True)


def test_str(mio):
    pass


def test_summary(mio):
    pass


def test_write(mio):
    pass


def test_writeln(mio):
    pass
