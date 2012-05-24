def test_clone(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}


def test_copy(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m copy") == {"a": 1, "b": 2}
    assert mio.eval("m id != (m copy id)")


def test_clear(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m clear") == None
    assert mio.eval("m") == {}


def test_repr(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert repr(mio.eval("m")) == "dict(a, 1, b, 2)"


def test_len(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m len") == 2


def test_get(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m get(\"a\")") == 1


def test_get_default(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m get(\"c\", 3)") == 3


def test_has(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m has(\"a\")") == True


def test_has_missing(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m has(\"c\")") == False


def test_set(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m set(\"c\", 3)") == {"a": 1, "b": 2, "c": 3}


def test_keys(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m keys") == ["a", "b"]


def test_values(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    assert mio.eval("m values") == [1, 2]


def test_items(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    items = list(mio.eval("m items"))
    items = [list(item) for item in items]
    assert items == [["a", 1], ["b", 2]]


def test_iter(mio):
    assert mio.eval("m = Dict clone") == {}
    assert mio.eval("m set(\"a\", 1)") == {"a": 1}
    assert mio.eval("m set(\"b\", 2)") == {"a": 1, "b": 2}

    items = list(iter(mio.eval("m")))
    items = [list(item) for item in items]
    assert items == [["a", 1], ["b", 2]]
