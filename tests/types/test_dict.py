from itertools import permutations


def test_null(mio):
    assert dict(iter(mio.eval("Dict"))) == {}


def test_clone(mio):
    assert mio.eval("Dict clone()") == {}


def test_clone_dict(mio):
    assert mio.eval("Dict clone(Dict clone() setitem(\"a\", 1))") == {"a": 1}


def test_repr(mio):
    assert repr(mio.eval("Dict")) == "dict()"


def test_repr2(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")

    assert repr(mio.eval("d")) in ["dict({0:s})".format(", ".join(p)) for p in permutations(["'a'=1", "'b'=2", "'c'=3"])]


def test_setitem(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d setitem(\"d\", 4)") == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_get(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d getitem(\"a\")") == 1


def test_len(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d len") == 3


def test_keys(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d keys")) == ["a", "b", "c"]


def test_values(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d setitem(\"a\", 1)")
    mio.eval("d setitem(\"b\", 2)")
    mio.eval("d setitem(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d values")) == [1, 2, 3]
