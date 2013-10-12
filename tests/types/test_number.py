def test_int(mio):
    assert int(mio.eval("1")) == 1


def test_float(mio):
    assert float(mio.eval("1.0")) == 1.0


def test_str(mio):
    assert str(mio.eval("1")) == "1"


def test_add(mio):
    assert mio.eval("1 + 2") == 3


def test_sub(mio):
    assert mio.eval("3 - 2") == 1


def test_mul(mio):
    assert mio.eval("3 * 2") == 6


def test_div(mio):
    assert mio.eval("1 / 2") == mio.eval("0.5")


def test_mod(mio):
    assert mio.eval("2 % 2") == 0


def test_mod2(mio):
    assert mio.eval("3 % 2") == 1


def test_pow(mio):
    assert mio.eval("2 ** 4") == 16
