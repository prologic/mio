def test(mio):
    mio.eval("i = 0")
    assert mio.eval("x = Continuation current; i += 1")
    assert mio.eval("i == 1")

    mio.eval("x call")
    assert mio.eval("i == 2")
