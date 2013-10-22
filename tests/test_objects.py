from pytest import raises

from mio import runtime
from mio.utils import format_object
from mio.errors import AttributeError, TypeError


def test_clone(mio):
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World parent") == runtime.find("Object")


def test_type(mio):
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World parent") == runtime.find("Object")
    assert mio.eval("World type") == "World"


def test_type1(mio):
    assert mio.eval("Object clone type") == "Object"


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


def test_while(mio):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]

    mio.eval("""
        sum = method(xs,
            i = 0
            sum = 0
            while (i < xs len,
                sum = sum + xs at(i)
                i += 1
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
    assert mio.eval("Foo has(\"x\")").value is True


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
    assert mio.eval("1 !=(0)").value is True


def test_println(mio, capsys):
    assert mio.eval("\"Hello World!\" println") == "Hello World!"
    out, err = capsys.readouterr()
    assert out == "Hello World!\n"


def test_set(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1
    assert mio.eval("Foo set(\"x\", 2)") == 2
    assert mio.eval("Foo x") == 2


def test_del(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo count = 1")
    assert mio.eval("Foo del(\"count\")").value is None

    with raises(AttributeError):
        mio.eval("Foo count", reraise=True)


def test_return1(mio):
    mio.eval("""x = method(return "foo"; "bar")""")
    assert mio.eval("x") == "foo"


def test_return2(mio):
    mio.eval("""x = method(
        return "foo"
        "bar"
    )""")

    assert mio.eval("x") == "foo"


def test_return3(mio):
    mio.eval("""x = method(
        y = method(
            return "foo"
        )
        return y
        "bar"
    )""")

    assert mio.eval("x") == "foo"


def test_return4(mio):
    mio.eval("""Number foo = method(

        (self)

    )""")

    assert mio.eval("1 foo") == 1


def test_return5(mio):
    mio.eval("""Number foo = method(
        (self < 2) ifTrue(return "foo")
        "bar"
    )""")

    assert mio.eval("1 foo") == "foo"
    assert mio.eval("2 foo") == "bar"


def test_summary(mio, capsys):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")

    assert mio.eval("Foo summary") == mio.eval("Foo")
    out, err = capsys.readouterr()
    assert out == "{0:s}\n".format(format_object(mio.eval("Foo")))


def test_write(mio, capsys):
    assert mio.eval("write(\"Hello World!\")").value is None
    out, err = capsys.readouterr()
    assert out == "Hello World!"


def test_write2(mio, capsys):
    assert mio.eval("write(\"a\", \"b\", \"c\")").value is None
    out, err = capsys.readouterr()
    assert out == "abc"


def test_writeln(mio, capsys):
    assert mio.eval("writeln(\"Hello World!\")").value is None
    out, err = capsys.readouterr()
    assert out == "Hello World!\n"


def test_writeln2(mio, capsys):
    assert mio.eval("writeln(\"a\", \"b\", \"c\")").value is None
    out, err = capsys.readouterr()
    assert out == "abc\n"


def test_repr(mio):
    assert mio.eval("1 repr") == "1"
    assert mio.eval("\"foo\" repr") == "'foo'"


def test_str(mio):
    assert mio.eval("1 str") == "1"
    assert mio.eval("\"foo\" str") == "foo"


def test_bool(mio):
    assert mio.eval("1 bool").value is True
    assert mio.eval("0 bool").value is False
    assert mio.eval("\"foo\" bool").value is True
    assert mio.eval("\"\" bool").value is False
