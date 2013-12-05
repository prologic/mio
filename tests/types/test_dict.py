from pytest import raises


from operator import itemgetter
from itertools import permutations


from mio.errors import KeyError


def test_null(mio):
    assert dict(iter(mio.eval("Dict"))) == {}


def test_clone(mio):
    assert mio.eval("Dict clone()") == {}


def test_hash(mio):
    l = mio.eval("Dict clone()")
    l.__hash__() is None


def test_clone_dict(mio):
    assert mio.frommio(mio.eval("Dict clone(Dict clone() __setitem__(\"a\", 1))")) == {u"a": 1}


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
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert mio.frommio(mio.eval("d __setitem__(\"d\", 4)")) == {u"a": 1, u"b": 2, u"c": 3, u"d": 4}


def test_getitem(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert mio.eval("d __getitem__(\"a\")") == 1


def test_getitem_KeyError(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    with raises(KeyError):
        mio.eval("d __getitem__(\"d\")", reraise=True)


def test_delitem(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert mio.frommio(mio.eval("d __delitem__(\"a\")")) == {u"b": 2, u"c": 3}


def test_len(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert mio.eval("d len") == 3


def test_len2(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert mio.eval("d __len__()") == 3


def test_len3(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert len(mio.eval("d")) == 3


def test_keys(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert sorted(mio.eval("d keys")) == [u"a", u"b", u"c"]


def test_values(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert sorted(mio.eval("d values")) == [1, 2, 3]


def test_items(mio):
    mio.eval("d = Dict clone()")
    mio.eval("d __setitem__(\"a\", 1)")
    mio.eval("d __setitem__(\"b\", 2)")
    mio.eval("d __setitem__(\"c\", 3)")
    assert mio.frommio(mio.eval("d")) == {u"a": 1, u"b": 2, u"c": 3}

    assert sorted(mio.frommio(mio.eval("d items")), key=itemgetter(0)) == [["a", 1], ["b", 2], ["c", 3]]
