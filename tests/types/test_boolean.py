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
    assert mio.eval("Boolean __repr__()") == repr(None)
    assert mio.eval("True __repr__()") == repr(True)
    assert mio.eval("False __repr__()") == repr(False)
    assert mio.eval("None __repr__()") == repr(None)
