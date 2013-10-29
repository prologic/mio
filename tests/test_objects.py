from pytest import raises


from itertools import permutations


from mio import runtime
from mio.utils import format_object
from mio.errors import AttributeError, TypeError


def test_clone(mio):
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World parent") == runtime.find("Object")


def test_type(mio):
    assert mio.eval("Object type") == "Object"
    assert mio.eval("1 type") == "Number"


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


def test_foreach2(mio, capfd):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]

    mio.eval("""
        xs foreach(x,
            (x == 2) ifTrue(continue) ifFalse(print(x))
        )
    """)
    out, err = capfd.readouterr()
    assert out == "1\n3\n"


def test_foreach3(mio, capfd):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]
    assert mio.eval("xs append(None)") == [1, 2, 3, None]
    assert mio.eval("xs append(4)") == [1, 2, 3, None, 4]
    assert mio.eval("xs append(5)") == [1, 2, 3, None, 4, 5]
    assert mio.eval("xs append(6)") == [1, 2, 3, None, 4, 5, 6]

    mio.eval("""
        xs foreach(x,
            (x is None) ifTrue(break) ifFalse(print(x))
        )
    """)
    out, err = capfd.readouterr()
    assert out == "1\n2\n3\n"


def test_foreach4(mio, capfd):
    assert mio.eval("d = Dict clone") == {}
    assert mio.eval("d set(\"a\", 1)") == {"a": 1}
    assert mio.eval("d set(\"b\", 2)") == {"a": 1, "b": 2}
    assert mio.eval("d set(\"c\", 3)") == {"a": 1, "b": 2, "c": 3}

    mio.eval("""
        d items foreach(k, v,
            print(k, "=", v, sep="")
        )
    """)
    out, err = capfd.readouterr()
    assert out in ["{0:s}\n".format("\n".join(p)) for p in permutations(["a=1", "b=2", "c=3"])]


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


def test_while2(mio):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]

    mio.eval("""
        i = 0
        sum = 0
        while (i < (xs len),
            (i == 2) ifTrue(i += 1; continue)
            sum = sum + xs at(i)
            i += 1
        )
    """)

    # XXX: The result here is wrong. continue doesn't work in whiel?
    #assert mio.eval("sum") == 4


def test_while3(mio):
    assert mio.eval("xs = List clone") == []
    assert mio.eval("xs append(1)") == [1]
    assert mio.eval("xs append(2)") == [1, 2]
    assert mio.eval("xs append(3)") == [1, 2, 3]
    assert mio.eval("xs append(None)") == [1, 2, 3, None]
    assert mio.eval("xs append(4)") == [1, 2, 3, None, 4]
    assert mio.eval("xs append(5)") == [1, 2, 3, None, 4, 5]
    assert mio.eval("xs append(6)") == [1, 2, 3, None, 4, 5, 6]

    mio.eval("""
        i = 0
        sum = 0
        while(i < (xs len),
            x = xs at(i)
            (x is None) ifTrue(break)
            sum += x
            i += 1
        )
    """)

    assert mio.eval("sum") == 6


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


def test_get_no_forward(mio):
    mio.eval("Foo = Object clone")
    mio.eval("Foo del(\"forward\")")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo get(\"x\")") == 1

    with raises(AttributeError):
        mio.eval("Foo z", reraise=True)


def test_has(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo has(\"x\")")


def test_has2(mio):
    mio.eval("Foo = Object clone")
    assert not mio.eval("Foo has(\"x\")")


def test_hash(mio):
    assert mio.eval("Object hash") == hash(runtime.find("Object"))


def test_id(mio):
    assert mio.eval("(Object id) == (Object id)")


def test_keys(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")
    assert mio.eval("Foo y = 2")
    keys = list(mio.eval("Foo keys"))
    assert "x" in keys
    assert "y" in keys


def test_method(mio):
    mio.eval("foo = method(1)")
    assert mio.eval("foo()") == 1

    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1") == 1

    mio.eval("Foo foo = method(self x)")
    assert mio.eval("Foo foo()") == 1


def test_neq(mio):
    assert mio.eval("1 !=(0)")


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
    assert mio.eval("x()") == "foo"


def test_return2(mio):
    mio.eval("""x = method(
        return "foo"
        "bar"
    )""")

    assert mio.eval("x()") == "foo"


def test_return3(mio):
    mio.eval("""x = method(
        y = method(
            return "foo"
        )
        return y()
        "bar"
    )""")

    assert mio.eval("x()") == "foo"


def test_return4(mio):
    mio.eval("""Number foo = method(

        (self)

    )""")

    assert mio.eval("1 foo()") == 1


def test_return5(mio):
    mio.eval("""Number foo = method(
        (self < 2) ifTrue(return "foo")
        "bar"
    )""")

    assert mio.eval("1 foo()") == "foo"
    assert mio.eval("2 foo()") == "bar"


def test_summary(mio, capfd):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo x = 1")

    assert mio.eval("Foo summary") == mio.eval("Foo")
    out, err = capfd.readouterr()
    assert out == "{0:s}\n".format(format_object(mio.eval("Foo")))


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
    assert mio.eval("1 repr") == "1"
    assert mio.eval("\"foo\" repr") == "'foo'"


def test_str(mio):
    assert mio.eval("1 str") == "1"
    assert mio.eval("\"foo\" str") == "foo"


def test_bool(mio):
    assert mio.eval("bool(1)")
    assert not mio.eval("bool(0)")
    assert mio.eval("bool(\"foo\")")
    assert not mio.eval("bool(\"\")")


def test_parent(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo parent is Object")


def test_parent2(mio):
    assert mio.eval("Object parent is Object")


def test_value(mio):
    assert mio.eval("Object value is None")


def test_setValue(mio):
    mio.eval("Foo = Object clone")
    assert mio.eval("Foo value is None")

    mio.eval("Foo setValue(1)")
    assert mio.eval("Foo value == 1")


def test_primitive(mio):
    mio.eval("Foo = Object :clone")
    assert not mio.eval("Foo is Object")


def test_primitive2(mio):
    with raises(AttributeError):
        mio.eval("Object :asdf", reraise=True)
