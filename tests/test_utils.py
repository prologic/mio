import sys
from mio.object import Object
from mio.utils import format_pymethod, format_object, pymethod, tryimport, Null


class Foo(Object):
        
    @pymethod()
    def noargs(self, receiver, context, m):
        pass

    @pymethod()
    def args(self, receiver, context, m, a, b, c):
        pass

    @pymethod()
    def varargs(self, receiver, context, m, *args):
        pass


FOO_TEMPLATE = """Foo_%s:
  args            = args(a, b, c)
  noargs          = noargs()
  varargs         = varargs(*args)"""


def test_format_object():
    foo = Foo()
    foo.create_methods()
    assert format_object(foo) == FOO_TEMPLATE % hex(id(foo))


def test_format_pymethod():
    foo = Foo()
    assert format_pymethod(foo.noargs) == "noargs()"
    assert format_pymethod(foo.args) == "args(a, b, c)"
    assert format_pymethod(foo.varargs) == "varargs(*args)"


def test_tryimport():
    m = tryimport("sys")
    assert m is sys


def test_tryimport_fail():
    try:
        m = tryimport("foo", "foo")
    except Warning as w:
        assert w[0] == "foo"


def test_null():
    assert Null is Null
    assert Null() is Null
