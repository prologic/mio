def test_bytes(mio):
    assert mio.eval('b"foo"') == "foo"


def test_bytes_type(mio):
    assert type(mio.eval('b"foo"').value) is str


def test_bytes_multi_line(mio):
    assert mio.eval('b"foo\nbar"') == "foo\nbar"


def test_bytes_single_quote(mio):
    assert mio.eval("b'foo'") == "foo"


def test_bytes_triple_single_quote(mio):
    assert mio.eval("b'''foo'''") == "foo"


def test_bytes_double_quote(mio):
    assert mio.eval('b"foo"') == "foo"


def test_bytes_triple_double_quote(mio):
    assert mio.eval('b"""foo"""') == "foo"


def test_init(mio):
    assert mio.eval("x = Bytes clone(b\"foo\")") == "foo"
    assert mio.eval("x") == "foo"


def test_iter(mio):
    assert list(iter(mio.eval("b\"foo\""))) == ["f", "o", "o"]


def test_int(mio):
    assert int(mio.eval("b\"1\"")) == 1


def test_float(mio):
    assert float(mio.eval("b\"1.0\"")) == 1.0


def test_str(mio):
    assert str(mio.eval("b\"foo\"")) == b"foo"


def test_unicode(mio):
    assert unicode(mio.eval("b\"foo\"")) == u"foo"


def test_repr(mio):
    assert repr(mio.eval("b\"foo\"")) == "b\"foo\""


def test_getitem(mio):
    assert mio.eval("b\"foo\" __getitem__(0) == b\"f\"")


def test_len(mio):
    assert mio.eval("b\"foo\" __len__()") == 3


def test_add(mio):
    assert mio.eval("b\"foo\" + b\"bar\"") == "foobar"


def test_mul(mio):
    assert mio.eval("b\"a\" * 4") == "aaaa"


def test_join(mio):
    assert mio.eval("b\",\" join([b\"1\", b\"2\", b\"3\"]) == b\"1,2,3\"")


def test_find(mio):
    assert mio.eval("b\"foobar\" find(b\"foo\")") == 0


def test_find2(mio):
    assert mio.eval("b\"foobar\" find(b\"foo\", 0, 1)") == -1


def test_lower(mio):
    assert mio.eval("b\"FOO\" lower()") == "foo"


def test_upper(mio):
    assert mio.eval("b\"foo\" upper()") == "FOO"
