from datetime import date


def test_ffi(mio):
    mio.eval('''
date = FFI clone("date", """
from datetime import date


__all__ = ("today",)


def today():
    return date.today().strftime("%B %d, %Y")
""")
    ''')

    today = date.today().strftime("%B %d, %Y")
    assert mio.eval("date today()") == today

    mio.eval("""del("date")""")


def test_ffi_repr(mio):
    mio.eval('''
foo = FFI clone("foo", """
def foo():
    return "Foobar!"
""")
    ''')

    assert repr(mio.eval("foo")) == "FFI(name='foo', file=None)"


def test_ffi_attrs(mio):
    mio.eval('''
foo = FFI clone("foo", """
x = 1


def foo():
    return "Foobar!"
""")
    ''')

    assert mio.eval("foo foo()") == "Foobar!"
    assert mio.eval("foo x") == 1


def test_ffi_fromfile(mio, tmpdir):
    with tmpdir.ensure("foo.py").open("w") as f:
        f.write('''
x = 1


def foo():
    return "Foobar!"
''')

    foo = mio.eval('foo = FFI fromfile("{0:s}")'.format(str(tmpdir.join("foo.py"))))
    assert foo.type == "FFI"
    assert foo.module is not None
    assert foo.name == "foo"
    assert foo.file == str(tmpdir.join("foo.py"))

    assert mio.eval("foo foo()") == "Foobar!"
    assert mio.eval("foo x") == 1


def test_ffi_importall(mio):
    mio.eval('''
date = FFI clone("date", """
from datetime import date


def foo():
    return "foo"


def today():
    return date.today().strftime("%B %d, %Y")


__all__ = ("today",)
""")
    ''')

    assert mio.eval("date keys") == ["today"]
