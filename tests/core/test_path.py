from pytest import raises


from os import getcwd, path


from mio.errors import TypeError
from mio.core.path import listdir


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


def test_join(mio):
    p = mio.eval("""p = Path clone("/tmp/foo")""")
    assert p.value == "/tmp/foo"

    pp = mio.eval("""pp = p join("bar.txt")""")
    assert pp.value == "/tmp/foo/bar.txt"


def test_open1(mio, tmpdir):
    foo = tmpdir.ensure("foo.txt")
    with foo.open("w") as f:
        f.write("Hello World!")

    p = mio.eval("""p = Path clone("{0:s}")""".format(str(foo)))
    assert p.value == str(foo)

    f = mio.eval("""f = p open("r")""")
    s = mio.eval("s = f read()")
    assert s == "Hello World!"


def test_open2(mio, tmpdir):
    p = mio.eval("""p = Path clone("{0:s}")""".format(str(tmpdir)))
    assert p.value == str(tmpdir)

    with raises(TypeError):
        mio.eval("""f = p open("r")""", reraise=True)


def test_list1(mio, tmpdir):
    tmpdir.ensure("foo.txt")
    tmpdir.ensure("bar.txt")

    p = mio.eval("""p = Path clone("{0:s}")""".format(str(tmpdir)))
    assert p.value == str(tmpdir)

    fs = mio.eval("fs = p list()")
    assert list(fs) == list(listdir(str(tmpdir)))


def test_list2(mio, tmpdir):
    tmpdir.ensure("foo.txt")
    tmpdir.ensure("bar.txt")
    tmpdir.ensure("baz.csv")

    p = mio.eval("""p = Path clone("{0:s}")""".format(str(tmpdir)))
    assert p.value == str(tmpdir)

    fs = mio.eval("""fs = p list("*.txt")""")
    assert list(fs) == list(listdir(str(tmpdir), "*.txt"))


def test_list3(mio, tmpdir):
    tmpdir.ensure("foo.txt")
    tmpdir.ensure("bar", dir=True).ensure("bar.txt")
    tmpdir.ensure("baz", dir=True).ensure("baz.txt")

    p = mio.eval("""p = Path clone("{0:s}")""".format(str(tmpdir)))
    assert p.value == str(tmpdir)

    fs = mio.eval("""fs = p list(None, True)""")
    assert list(fs) == list(listdir(str(tmpdir), rec=True))
