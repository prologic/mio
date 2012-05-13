def test_clone(mio):
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World type") == "World"


def test_mixin(mio):
    mio.eval("Base = Object clone")
    mio.eval("Base a = 1")
    mio.eval("World = Object clone")
    assert mio.eval("World")
    assert mio.eval("World type") == "World"

    mio.eval("World mixin(Base)")
    assert mio.eval("World a") == 1
