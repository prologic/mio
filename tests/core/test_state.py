from mio.utils import Null


def test_repr1(mio):
    mio.eval("f = block(State clone())")
    assert repr(mio.eval("f()")) == "NormalState()"


def test_repr2(mio):
    mio.eval("f = block(State clone() setBreak())")
    assert repr(mio.eval("f()")) == "BreakState()"


def test_repr3(mio):
    mio.eval("f = block(State clone() setContinue())")
    assert repr(mio.eval("f()")) == "ContinueState()"


def test_repr4(mio):
    mio.eval("f = block(State clone() setReturn())")
    assert repr(mio.eval("f()")) == "ReturnState()"


def test_repr5(mio):
    mio.eval("f = block(State clone() setReturn(\"foo\"))")
    assert repr(mio.eval("f()")) == "ReturnState(u\"foo\")"


def test_reset(mio):
    mio.eval("f = block(State clone() setReturn(\"foo\"))")
    state = mio.eval("f()")
    assert state.isReturn
    assert state.value == "foo"
    assert repr(state) == "ReturnState(u\"foo\")"

    state.reset()
    assert not state.isReturn
    assert state.value is Null
    assert repr(state) == "NormalState()"


def test_state_stop(mio):
    mio.eval("f = block(State clone() setReturn(\"foo\"))")
    assert mio.eval("f() stop()")


def test_state_invalid(mio):
    assert mio.eval("state setContinue() is state")


def test_state_invalid2(mio):
    assert mio.eval("state setReturn() is state")


def test_state_invalid3(mio):
    assert mio.eval("state setBreak() is state")
