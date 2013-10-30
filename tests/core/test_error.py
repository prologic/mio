def test_error(mio):
    mio.eval("""e = Error clone("Foo", "FooBar!")""")
    assert mio.eval("e error") == "Foo"
    assert mio.eval("e message") == "FooBar!"


def test_exception(mio):
    mio.eval("e = Exception try(a + b)")
    assert mio.eval("e error") == "AttributeError"
    assert mio.eval("e message") == "Object has no attribute 'a'"


def test_isError(mio):
    mio.eval("e = Exception try(a + b)")
    assert mio.eval("e isError")


def test_ifError(mio):
    mio.eval("e = Exception try(a + b)")
    assert mio.eval("e ifError(True)")
