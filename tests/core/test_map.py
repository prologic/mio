def test_clone(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}


def test_copy(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    n = mio.eval("m copy")
    assert id(n) is not id(m)
    assert n == {"a": 1, "b": 2}


def test_clone(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m clear") == None
    assert m == {}


def test_repr(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert repr(m) == "map(a, 1, b, 2)"


def test_len(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m len") == 2


def test_get(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m get(\"a\")") == 1


def test_get_default(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m get(\"c\", 3)") == 3


def test_has(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m has(\"a\")") == True


def test_has_missing(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m has(\"c\")") == False


def test_set(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m set(\"c\", 3)") == {"a": 1, "b": 2, "c": 3}


def test_keys(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m keys") == ["a", "b"]


def test_values(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    assert mio.eval("m values") == [1, 2]


def test_items(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    items = list(mio.eval("m items"))
    items = [list(item) for item in items]
    assert items == [["a", 1], ["b", 2]]


def test_iter(mio):
    m = mio.eval("m = Map clone(\"a\", 1, \"b\", 2)")
    assert m == {"a": 1, "b": 2}

    items = list(iter(m))
    items = [list(item) for item in items]
    assert items == [["a", 1], ["b", 2]]
