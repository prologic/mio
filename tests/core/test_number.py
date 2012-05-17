def test_add(mio):
    assert mio.eval("1 + 2") == 3


def test_sub(mio):
    assert mio.eval("3 - 2") == 1


def test_mul(mio):
    assert mio.eval("3 * 2") == 6


def test_div(mio):
    assert mio.eval("1 / 2") == mio.eval("0.5")
