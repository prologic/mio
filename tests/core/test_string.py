def test_string(mio):
    assert mio.eval("\"foo\"") == "foo"


def test_int(mio):
    assert int(mio.eval("\"1\"")) == 1


def test_float(mio):
    assert float(mio.eval("\"1.0\"")) == 1.0


def test_str(mio):
    assert str(mio.eval("\"foo\"")) == "foo"


def test_add(mio):
    assert mio.eval("\"foo\" + \"bar\"") == "foobar"


def test_mul(mio):
    assert mio.eval("\"a\" * 4") == "aaaa"


def test_find(mio):
    assert mio.eval("\"foobar\" find(\"foo\")") == 0


def test_find2(mio):
    assert mio.eval("\"foobar\" find(\"foo\", 0, 1)") == -1
