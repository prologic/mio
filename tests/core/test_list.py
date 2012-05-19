def test_clone(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]


def test_repr(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert repr(l) == "list(1, 2, 3)"


def test_append(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    mio.eval("l append(4)")
    assert l == [1, 2, 3, 4]


def test_at(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    assert mio.eval("l at(0)") == 1


def test_len(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    assert mio.eval("l len") == 3


def test_count(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    assert mio.eval("l count(1)") == 1


def test_extend(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    assert mio.eval("l extend(4, 5, 6)") == [1, 2, 3, 4, 5, 6]


def test_reverse(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    mio.eval("l reverse")
    assert l == [3, 2, 1]


def test_reversed(mio):
    l = mio.eval("l = List clone(1, 2, 3)")
    assert l == [1, 2, 3]

    assert list(mio.eval("l reversed")) == [3, 2, 1]


def test_sort(mio):
    l = mio.eval("l = List clone(3, 1, 2)")
    assert l == [3, 1, 2]

    mio.eval("l sort")
    assert l == [1, 2, 3]


def test_sorted(mio):
    l = mio.eval("l = List clone(3, 1, 2)")
    assert l == [3, 1, 2]

    assert mio.eval("l sorted") == [1, 2, 3]
