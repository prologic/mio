from os import getcwd, path


def test_path(mio):
    p = mio.eval("Path")
    assert p.value == getcwd()


def test_repr(mio):
    assert repr(mio.eval("Path")) == "Path({0:s})".format(repr(unicode(getcwd())))


def test_str(mio):
    assert str(mio.eval("Path")) == str(getcwd())


def test_clone1(mio):
    p = mio.eval("""Path clone("/tmp/foo.txt")""")
    assert p.value == "/tmp/foo.txt"


def test_clone2(mio):
    p = mio.eval("""Path clone("~/foo.txt", True)""")
    assert p.value == path.expanduser("~/foo.txt")
