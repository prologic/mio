import sys
from mio.object import Object
from mio.utils import format_method, format_object, method, tryimport, Null


class Foo(Object):
        
    @method()
    def noargs(self, receiver, context, m):
        pass

    @method()
    def args(self, receiver, context, m, a, b, c):
        pass

    @method()
    def varargs(self, receiver, context, m, *args):
        pass


FOO_TEMPLATE = """Foo:
  args            = args(a, b, c)
  noargs          = noargs()
  varargs         = varargs(*args)"""


def test_format_object():
    foo = Foo()
    foo.create_methods()
    assert format_object(foo) == FOO_TEMPLATE


def test_format_method():
    foo = Foo()
    assert format_method(foo.noargs) == "noargs()"
    assert format_method(foo.args) == "args(a, b, c)"
    assert format_method(foo.varargs) == "varargs(*args)"


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
