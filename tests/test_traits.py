from pytest import raises


from mio.errors import AttributeError, TypeError


def test_basic_trait(mio, capfd):
    mio.eval("""
        TGreeting = Trait clone() do (
            hello = method(
                print("Hello", self getGreeting())
            )
        )

        World = Object clone() do (
            use(TGreeting)

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


def test_basic_trait2(mio, capfd):
    mio.eval("""
        TGreeting = Trait clone() do (
            hello = method(
                print("Hello", self getGreeting())
            )
        )

        World = Object clone() do (
            use(TGreeting)

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

    with raises(TypeError):
        mio.eval("World use(TGreeting)", reraise=True)


def test_invalid(mio):
    mio.eval("TGreetable = Object clone()")

    with raises(TypeError):
        mio.eval("Object clone() use(TGreetable)", reraise=True)


def test_state(mio):
    mio.eval("TGreetable = Trait clone()")

    with raises(TypeError):
        mio.eval("TGreetable greeting = \"World!\"", reraise=True)


def test_requirements(mio):
    mio.eval("""
        TGreetable = Trait clone() do(
            requires("greeting")
        )
    """)

    mio.eval("TGreetable requirements()") == [u"greeting"]


def test_requires(mio):
    mio.eval("""
        TGreetable = Trait clone() do(
            requires("greeting")
        )
    """)

    with raises(TypeError):
        mio.eval("Object clone() use(TGreetable)", reraise=True)


def test_resolution(mio):
    mio.eval("""
        TFoo = Trait clone() do(
            foo = method("foo")
        )
        TBar = Trait clone() do(
            foo = method("foo")
        )
    """)

    with raises(TypeError):
        mio.eval("Object clone() use(TFoo) use(TBar)", reraise=True)


def test_resolution2(mio):
    mio.eval("""
        TFoo = Trait clone() do(
            foo = method("foo")
        )
        TBar = Trait clone() do(
            foo = method("foo")
        )
    """)

    mio.eval("Foo = Object clone() use(TFoo) use(TBar, {\"foo\": \"bar\"})")
    assert mio.eval("Foo hasTrait(TFoo)")
    assert mio.eval("Foo hasTrait(TBar)")
    assert mio.eval("Foo behaviors") == ["foo", "bar"]


def test_resolution_deltrait(mio):
    mio.eval("""
        TFoo = Trait clone() do(
            foo = method("foo")
        )
        TBar = Trait clone() do(
            foo = method("foo")
        )
    """)

    mio.eval("Foo = Object clone() use(TFoo) use(TBar, {\"foo\": \"bar\"})")
    assert mio.eval("Foo hasTrait(TFoo)")
    assert mio.eval("Foo hasTrait(TBar)")
    assert mio.eval("Foo behaviors") == ["foo", "bar"]

    mio.eval("Foo delTrait(TFoo)")
    assert not mio.eval("Foo hasTrait(TFoo)")
    assert mio.eval("Foo behaviors") == ["bar"]

    mio.eval("Foo delTrait(TBar)")
    assert not mio.eval("Foo hasTrait(TBar)")
    assert mio.eval("Foo behaviors") == []


def test_adapt(mio):
    mio.eval("TGreetable = Trait clone()")
    assert mio.eval("World = Object clone() adapt(TGreetable) hasTrait(TGreetable)")


def test_hasTrait(mio):
    mio.eval("""
        TGreetable = Trait clone()
        World = Object clone() do (
            use(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")


def test_hasTrait2(mio):
    mio.eval("""
        TGreetable = Trait clone()
        World = Object clone() do (
            use(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")
    assert mio.eval("World clone() hasTrait(TGreetable)")


def test_delTrait(mio):
    mio.eval("""
        TGreetable = Trait clone()
        World = Object clone() do (
            use(TGreetable)
        )
    """)

    assert mio.eval("World hasTrait(TGreetable)")
    mio.eval("World delTrait(TGreetable)")
    assert mio.eval("World behaviors") == []
    assert not mio.eval("World hasTrait(TGreetable)")


def test_delTrait2(mio, capfd):
    mio.eval("""
        TGreetable = Trait clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            use(TGreetable)
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


def test_delTrait3(mio, capfd):
    mio.eval("""
        TGreetable = Trait clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            use(TGreetable)
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

    with raises(TypeError):
        mio.eval("World delTrait(TGreetable)", reraise=True)


def test_traits(mio):
    mio.eval("""
        TGreetable = Trait clone()
        World = Object clone() do (
            use(TGreetable)
        )
    """)

    TGreetable = mio.eval("TGreetable")
    assert mio.eval("World traits") == [TGreetable]


def test_behaviors(mio, capfd):
    mio.eval("""
        TGreetable = Trait clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            use(TGreetable)
        )
    """)

    assert mio.eval("World hello()").value is None
    out, err = capfd.readouterr()
    assert out == "Hello World!\n"
    assert mio.eval("World behaviors") == ["hello"]


def test_del_behavior(mio, capfd):
    mio.eval("""
        TGreetable = Trait clone() do (
            hello = method(
                print("Hello World!")
            )
        )

        World = Object clone() do (
            use(TGreetable)
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
