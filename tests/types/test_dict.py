from itertools import permutations


def test_null(mio):
    assert dict(iter(mio.eval("Dict"))) == {}


def test_clone(mio):
    assert mio.eval("Dict clone") == {}


def test_clone_dict(mio):
    assert mio.eval("Dict clone(Dict clone set(\"a\", 1))") == {"a": 1}


def test_repr(mio):
    assert repr(mio.eval("Dict")) == "Dict"


def test_repr2(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")

    assert repr(mio.eval("d")) in ["dict({0:s})".format(", ".join(p)) for p in permutations(["'a'=1", "'b'=2", "'c'=3"])]


def test_set(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d set(\"d\", 4)") == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_get(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d get(\"a\")") == 1


def test_len(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert mio.eval("d len") == 3


def test_keys(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d keys")) == ["a", "b", "c"]


def test_values(mio):
    mio.eval("d = Dict clone")
    mio.eval("d set(\"a\", 1)")
    mio.eval("d set(\"b\", 2)")
    mio.eval("d set(\"c\", 3)")
    assert mio.eval("d") == {"a": 1, "b": 2, "c": 3}

    assert sorted(mio.eval("d values")) == [1, 2, 3]
