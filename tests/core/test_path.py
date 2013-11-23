from os import getcwd


def test_path(mio):
    p = mio.eval("Path")
    assert p.value == getcwd()


def test_repr(mio):
    assert repr(mio.eval("Path")) == "Path({0:s})".format(repr(unicode(getcwd())))


def test_str(mio):
    assert str(mio.eval("Path")) == str(getcwd())
