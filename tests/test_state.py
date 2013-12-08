from pytest import raises


from decimal import Decimal


from mio import runtime
from mio.utils import Null
from mio.state import Completer
from mio.errors import AttributeError, Error


# Supported Types
# {
#     dict:    "Dict"
#     list:    "List"
#     tuple:   "Tuple",
#     unicode: "String"
#     str:     "Bytes",
#     bool:    "Boolean"
#     Decimal: "Number"
# }


class Foo(object):
    """Foo Class

    mio does not support coerving Python user classes, methods or
    objects. Trying to convert these to mio with ``runtime.state.tomio(...)``
    will fail and if a ``default`` value is passed will return that.
    """

    def foo(self):
        """foo method"""


def test_tomio_class(mio):
    assert runtime.state.tomio(Foo, Null) is Null


def test_tomio_object(mio):
    foo = Foo()
    assert runtime.state.tomio(foo, Null) is Null


def test_tomio_method(mio):
    foo = Foo()
    assert runtime.state.tomio(foo.foo, Null) is Null


def test_frommio_Number(mio):
    assert runtime.state.frommio(mio.eval("1.0")) == Decimal(1.0)


def test_tomio_Number(mio):
    assert runtime.state.tomio(1.0) == mio.eval("1.0")


def test_frommio_Boolean(mio):
    assert runtime.state.frommio(mio.eval("True")) is True


def test_tomio_Boolean(mio):
    # XXX: FIXME: This should be the same identity
    assert runtime.state.tomio(True) == mio.eval("True")


def test_frommio_String(mio):
    assert runtime.state.frommio(mio.eval("String clone()")) == ""


def test_tomio_String(mio):
    assert runtime.state.tomio("") == mio.eval("String clone()")


def test_frommio_List(mio):
    assert runtime.state.frommio(mio.eval("List clone()")) == []


def test_tomio_List(mio):
    assert runtime.state.tomio([]) == mio.eval("List clone()")


def test_frommio_Tuple(mio):
    assert runtime.state.frommio(mio.eval("Tuple clone()")) == ()


def test_tomio_Tuple(mio):
    assert runtime.state.tomio(()) == mio.eval("Tuple clone()")


def test_frommio_Dict(mio):
    assert runtime.state.frommio(mio.eval("Dict clone()")) == {}


def test_tomio_Dict(mio):
    assert runtime.state.tomio({}) == mio.eval("Dict clone()")


def test_tomio_default(mio):
    assert runtime.state.frommio(runtime.state.tomio(type(None))) is None


def test_error(mio, capfd):
    with raises(AttributeError):
        mio.eval("foobar()", reraise=True)
    out, err = capfd.readouterr()
    assert out == "\n  AttributeError: Object has no attribute 'foobar'\n  ---------------\n  foobar\n\n"


def test_usererror(mio, capfd):
    with raises(Error):
        mio.eval("raise TypeError", reraise=True)
    out, err = capfd.readouterr()
    assert out == "\n  TypeError: \n  ----------\n  raise(TypeError)\n\n"


def test_runsource(mio):
    assert runtime.state.runsource("(1 + 2")


def test_runsource2(mio, capfd):
    assert runtime.state.runsource("(1 + 2)") is None

    out, err = capfd.readouterr()
    assert out == "===> 3\n"


def test_completer(mio):
    completer = Completer(mio)

    assert completer.complete("", 0) == "Core"


def test_completer2(mio):
    completer = Completer(mio)

    assert completer.complete("Root ", 0) == "Root Core"


def test_completer3(mio):
    completer = Completer(mio)

    assert completer.complete("Root bu", 0) == "Root builtins"


def test_completer4(mio):
    completer = Completer(mio)

    assert completer.complete("Root asdf ", 0) is None


def test_completer5(mio):
    completer = Completer(mio)
    assert completer.complete("", 0) == "Core"

    assert completer.complete("", len(completer.matches)) is None


def test_completer6(mio, capfd):
    completer = Completer(mio)

    completer.display_matches("Root", ["Root Core", "Root Types"], 10)

    out, err = capfd.readouterr()
    assert out == "\n Core        Types      \nmio> "


def test_completer7(mio, capfd):
    completer = Completer(mio)

    completer.display_matches("Root", ["Root Core"] * 100, 9)

    out, err = capfd.readouterr()
    assert set(out.split()[:-1]) == set(["Core"])
