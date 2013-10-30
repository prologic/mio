def test_exception(mio):
    mio.eval("e = Exception try(a + b)")
    assert mio.eval("e error") == "AttributeError"
    assert mio.eval("e message") == "Object has no attribute 'a'"
