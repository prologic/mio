def test_null(mio):
    assert list(iter(mio.eval("List"))) == []


def test_clone(mio):
    assert mio.eval("List clone()") == []


def test_clone_list(mio):
    assert mio.eval("List clone(List clone() append(1))") == [1]


def test_repr(mio):
    assert repr(mio.eval("List")) == "[]"


def test_repr2(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")

    assert repr(mio.eval("xs")) == "[1, 2, 3]"


def test_append(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs append(4)") == [1, 2, 3, 4]


def test_at(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs at(0)") == 1


def test_getitem(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs __getitem__(0)") == 1


def test_len(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs len") == 3


def test_len2(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs __len__()") == 3


def test_len3(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert len(mio.eval("xs")) == 3


def test_count(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs count(1)") == 1


def test_extend(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs extend(4, 5, 6)") == [1, 2, 3, 4, 5, 6]


def test_reverse(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    mio.eval("xs reverse()")
    assert mio.eval("xs") == [3, 2, 1]


def test_reversed(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    mio.eval("xs append(3)")
    assert mio.eval("xs") == [1, 2, 3]

    assert mio.eval("xs reversed()") == [3, 2, 1]


def test_sort(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(3)")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    assert mio.eval("xs") == [3, 1, 2]

    mio.eval("xs sort()")
    assert mio.eval("xs") == [1, 2, 3]


def test_sorted(mio):
    mio.eval("xs = List clone()")
    mio.eval("xs append(3)")
    mio.eval("xs append(1)")
    mio.eval("xs append(2)")
    assert mio.eval("xs") == [3, 1, 2]

    assert mio.eval("xs sorted()") == [1, 2, 3]
