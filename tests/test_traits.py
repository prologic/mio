from pytest import raises


from mio.errors import AttributeError


def test_basic_trait(mio, capfd):
    mio.eval("""
        TGreeting = Object clone() do (
            hello = method(
                print("Hello", self getGreeting())
            )
        )

        World = Object clone() do (
            uses(TGreeting)

            greeting = "World!"

            getGreeting = method(
               self greeting
            )

            setGreeting = method(aGreeting,
                self greeting = aGreeting
            )
        )
    """)

    mio.eval("World hello()")
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("World setGreeting(\"John\")")
    mio.eval("World hello()")
    out, err = capfd.readouterr()
    assert out == "Hello John\n"


def test_hasTrait(mio):
    mio.eval("""
        TGreetable = Object clone()
        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")


def test_delTrait(mio):
    mio.eval("""
        TGreetable = Object clone()
        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")
    mio.eval("World delTrait(TGreetable)")
    assert mio.eval("World behaviors") == []
    assert not mio.eval("World hasTrait(TGreetable)")


def test_delTrait2(mio, capfd):
    mio.eval("""
        TGreetable = Object clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")
    assert mio.eval("World behaviors") == ["hello"]

    assert mio.eval("World hello()").value is None
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("World delTrait(TGreetable)")
    assert mio.eval("World behaviors") == []
    assert not mio.eval("World hasTrait(TGreetable)")

    with raises(AttributeError):
        mio.eval("World hello()", reraise=True)


def test_addTrait(mio):
    mio.eval("""
        TGreetable = Object clone()
        World = Object clone()
    """)

    assert not mio.eval("World hasTrait(TGreetable)")
    mio.eval("World addTrait(TGreetable)")
    assert mio.eval("World hasTrait(TGreetable)")


def test_traits(mio):
    mio.eval("""
        TGreetable = Object clone()
        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    TGreetable = mio.eval("TGreetable")
    assert mio.eval("World traits") == [TGreetable]


def test_behaviors(mio, capfd):
    mio.eval("""
        TGreetable = Object clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    assert mio.eval("World hello()").value is None
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"
    assert mio.eval("World behaviors") == ["hello"]


def test_del_behavior(mio, capfd):
    mio.eval("""
        TGreetable = Object clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            uses(TGreetable)
        )
    """)

    assert mio.eval("World hello()").value is None
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"
    assert mio.eval("World behaviors") == ["hello"]

    mio.eval("World del(\"hello\")")

    with raises(AttributeError):
        mio.eval("World hello()", reraise=True)
    assert mio.eval("World behaviors") == []
