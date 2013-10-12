def test_range_start(mio):
    assert mio.eval("Range clone(3)") == [0, 1, 2]


def test_range_stop(mio):
    assert mio.eval("Range clone(2, 4)") == [2, 3]


def test_range_stop(mio):
    assert mio.eval("Range clone(2, 8, 2)") == [2, 4, 6]


def test_range_iter(mio):
    assert list(iter(mio.eval("Range clone(3)"))) == [0, 1, 2]


def test_range_str(mio):
    assert str(mio.eval("Range clone(3)")) == "[0, 1, 2]"
