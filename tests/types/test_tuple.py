def test_null(mio):
    assert tuple(iter(mio.eval("Tuple"))) == ()


def test_clone(mio):
    assert mio.eval("Tuple clone()") == ()


#XXX: Broken
#def test_clone_tuple(mio):
#    assert mio.eval("Tuple clone(Tuple clone((1, 2, 3)))") == (1, 2, 3)


def test_repr(mio):
    assert repr(mio.eval("Tuple")) == "()"


def test_repr2(mio):
    mio.eval("xs = (1, 2, 3)")
    assert repr(mio.eval("xs")) == "(1, 2, 3)"


def test_at(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs at(0)") == 1


def test_getitem(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs __getitem__(0)") == 1


def test_len(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs len") == 3


def test_len2(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs __len__()") == 3


def test_len3(mio):
    xs = mio.eval("(1, 2, 3)")
    assert len(xs) == 3


def test_count(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs count(1)") == 1


def test_reversed(mio):
    mio.eval("xs = (1, 2, 3)")
    assert mio.eval("xs") == (1, 2, 3)
    assert mio.eval("xs reversed()") == (3, 2, 1)


def test_sorted(mio):
    mio.eval("xs = (3, 1, 2)")
    assert mio.eval("xs") == (3, 1, 2)
    assert mio.eval("xs sorted()") == (1, 2, 3)
