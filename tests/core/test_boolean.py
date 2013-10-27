from mio.utils import Null


def test_boolean(mio):
    assert mio.eval("Boolean").value is Null
    assert mio.eval("True").value is True
    assert mio.eval("False").value is False
    assert mio.eval("None").value is None


def test_init(mio):
    assert mio.eval("Boolean clone is Boolean")
    assert mio.eval("True clone is True")
    assert mio.eval("False clone is False")
    assert mio.eval("None clone is None")


def test_repr(mio):
    Boolean = mio.eval("Boolean")
    assert repr(mio.eval("Boolean")) == "Boolean at {0:s}".format(hex(id(Boolean)))
    assert repr(mio.eval("True")) == repr(True)
    assert repr(mio.eval("False")) == repr(False)
    assert repr(mio.eval("None")) == repr(None)
