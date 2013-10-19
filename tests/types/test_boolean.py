def test_boolean(mio):
    assert mio.eval("Boolean").value is None
    assert mio.eval("True").value is True
    assert mio.eval("False").value is False
    assert mio.eval("None").value is None


def test_init(mio):
    assert mio.eval("Boolean clone is Boolean")
    assert mio.eval("True clone is True")
    assert mio.eval("False clone is False")
    assert mio.eval("None clone is None")


def test_repr(mio):
    assert repr(mio.eval("Boolean")) == repr(None)
    assert repr(mio.eval("True")) == repr(True)
    assert repr(mio.eval("False")) == repr(False)
    assert repr(mio.eval("None")) == repr(None)
