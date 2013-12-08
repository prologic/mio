from pytest import raises

from mio.errors import IndexError


def test_range_init(mio):
    mio.eval("xs = List clone()") == []
    mio.eval("xs append(2)") == [2]
    mio.eval("xs append(8)") == [2, 8]
    mio.eval("xs append(2)") == [2, 8, 2]
    assert mio.eval("xs") == [2, 8, 2]

    assert mio.eval("list(Range clone(*xs))") == [2, 4, 6]


def test_range_start(mio):
    assert mio.eval("list(Range clone(3))") == [0, 1, 2]


def test_range_stop(mio):
    assert mio.eval("list(Range clone(2, 4))") == [2, 3]


def test_range_step(mio):
    assert mio.eval("list(Range clone(2, 8, 2))") == [2, 4, 6]


def test_range_setStep(mio):
    mio.eval("r = Range clone(2, 8, 2)")
    assert mio.eval("list(r)") == [2, 4, 6]

    mio.eval("r setStep(1)")
    assert mio.eval("list(r)") == [2, 3, 4, 5, 6, 7]


def test_range_invalid(mio):
    assert mio.eval("list(Range clone(10, 0, 1))") == []


def test_range_invalid2(mio):
    assert mio.eval("list(Range clone(0, 10, -1))") == []


def test_range_getitem(mio):
    mio.eval("r = Range clone(3)")
    assert mio.eval("r __getitem__(0)") == 0
    assert mio.eval("r __getitem__(1)") == 1
    assert mio.eval("r __getitem__(2)") == 2
    assert mio.eval("r __getitem__(3)") == 3


def test_range_getitem2(mio):
    mio.eval("r = Range clone(3)")
    assert mio.eval("r __getitem__(0)") == 0
    assert mio.eval("r __getitem__(1)") == 1
    assert mio.eval("r __getitem__(2)") == 2
    assert mio.eval("r __getitem__(3)") == 3

    with raises(IndexError):
        mio.eval("r __getitem__(4)", reraise=True)


def test_range_getitem3(mio):
    assert mio.eval("Range clone(10, 0, 1) __getitem__(0)") == 10


def test_range_repr(mio):
    assert repr(mio.eval("Range clone(3)")) == "range(3)"


def test_range_str(mio):
    assert str(mio.eval("Range clone(3)")) == "range(3)"
