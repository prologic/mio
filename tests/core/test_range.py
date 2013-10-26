def test_range_init(mio):
    mio.eval("xs = List clone") == []
    mio.eval("xs append(2)") == [2]
    mio.eval("xs append(8)") == [2, 8]
    mio.eval("xs append(2)") == [2, 8, 2]
    assert mio.eval("xs") == [2, 8, 2]

    assert mio.eval("Range clone(xs) asList") == [2, 4, 6]


def test_range_start(mio):
    assert mio.eval("Range clone(3) asList") == [0, 1, 2]


def test_range_stop(mio):
    assert mio.eval("Range clone(2, 4) asList") == [2, 3]


def test_range_step2(mio):
    assert mio.eval("Range clone(2, 8, 2) asList") == [2, 4, 6]


def test_range_invalid(mio):
    assert mio.eval("Range clone(10, 0, 1) asList") == []


def test_range_invalid2(mio):
    assert mio.eval("Range clone(0, 10, -1) asList") == []


def test_range_iter(mio):
    assert list(iter(mio.eval("Range clone(3)"))) == [0, 1, 2]


def test_range_repr(mio):
    assert repr(mio.eval("Range clone(3)")) == "range(3)"


def test_range_str(mio):
    assert str(mio.eval("Range clone(3)")) == "range(3)"


def test_range_asList(mio):
    assert mio.eval("Range clone(3) asList") == [0, 1, 2]