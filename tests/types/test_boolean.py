def test_boolean(mio):
    assert mio.eval("Boolean").value is None
    assert mio.eval("True")
    assert not mio.eval("False")
    assert mio.eval("None").value is None


def test_init(mio):
    assert mio.eval("Boolean clone() is Boolean")
    assert mio.eval("True clone() is True")
    assert mio.eval("False clone() is False")
    assert mio.eval("None clone() is None")


def test_repr(mio):
    assert mio.eval("Boolean repr") == repr(None)
    assert mio.eval("True repr") == repr(True)
    assert mio.eval("False repr") == repr(False)
    assert mio.eval("None repr") == repr(None)
