from itertools import permutations


def test_null(mio):
    assert dict(iter(mio.eval("Dict"))) == {}


def test_clone(mio):
    assert mio.eval("Dict clone()") == {}


def test_clone_dict(mio):
    assert mio.eval("Dict clone(Dict clone() __setitem__(\"a\", 1))") == {"a": 1}


def test_repr(mio):
    assert repr(mio.eval("Dict")) == "{}"


def test_repr2(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")

    assert repr(mio.eval("d")) in ["{" + ", ".join(p) + "}" for p in permutations(["u\"a\": 1", "u\"b\": 2", "u\"c\": 3"])]


def test_setitem(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d __setitem__(\"d\", 4)") == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_getitem(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d __getitem__(\"a\")") == 1


def test_len(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d len") == 3


def test_keys(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d keys")) == ["a", "b", "c"]


def test_values(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d values")) == [1, 2, 3]
