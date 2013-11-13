def test_int(mio):
    assert int(mio.eval("1")) == 1


def test_negative_int(mio):
    assert int(mio.eval("-1")) == -1


def test_e_int(mio):
    assert int(mio.eval("1e3")) == 1000


def test_int2(mio):
    assert mio.eval("1.5 int()") == 1


def test_float(mio):
    assert float(mio.eval("1.0")) == 1.0


def test_negative_float(mio):
    assert float(mio.eval("-1.0")) == -1.0


def test_e_float(mio):
    assert float(mio.eval("1.0e3")) == 1000.0


def test_float2(mio):
    assert mio.eval("1 float()") == 1.0


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


def test_primitive_abs(mio):
    assert mio.eval("""Number clone() setValue(-1 :("__abs__")) == 1""")
    assert mio.eval("""Number clone() setValue(1 :("__abs__")) == 1""")
