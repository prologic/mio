from decimal import Decimal


from mio import runtime


# Supported Types
# {
#     dict:    "Dict"
#     list:    "List"
#     str:     "String"
#     bool:    "Boolean"
#     Decimal: "Number"
# }


def test_frommio_Number(mio):
    assert runtime.state.frommio(mio.eval("1.0")) == Decimal(1.0)


def test_tomio_Number(mio):
    assert runtime.state.tomio(1.0) == mio.eval("1.0")


def test_frommio_Boolean(mio):
    assert runtime.state.frommio(mio.eval("True")) is True


def test_tomio_Boolean(mio):
    assert runtime.state.tomio(True) is mio.eval("True")


def test_frommio_String(mio):
    assert runtime.state.frommio(mio.eval("String clone")) == ""


def test_tomio_String(mio):
    assert runtime.state.tomio("") == mio.eval("String clone")


def test_frommio_List(mio):
    assert runtime.state.frommio(mio.eval("List clone")) == []


def test_tomio_List(mio):
    assert runtime.state.tomio([]) == mio.eval("List clone")


def test_frommio_Dict(mio):
    assert runtime.state.frommio(mio.eval("Dict clone")) == {}


def test_tomio_Dict(mio):
    assert runtime.state.tomio({}) == mio.eval("Dict clone")
