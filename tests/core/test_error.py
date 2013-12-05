def test_error(mio):
    mio.eval("""e = Error clone("Foo", "FooBar!")""")
    assert mio.eval("e type") == "Foo"
    assert mio.eval("e message") == "FooBar!"


def test_call(mio):
    mio.eval("""e = Error("FooBar!")""")
    assert mio.eval("e message == \"FooBar!\"")


def test_repr(mio):
    e = mio.eval("""Error clone("Foo", "FooBar!")""")
    assert repr(e) == "Foo(FooBar!)"


def test_exception(mio):
    mio.eval("e = Exception try(a + b)")
    assert mio.eval("e type") == "AttributeError"
    assert mio.eval("e message") == "Object has no attribute 'a'"
