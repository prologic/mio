from mio.message import Message


def test_name(mio):
    m = Message("foo")
    assert m.name == "foo"


def test_args(mio):
    args = [Message("%d" % i) for i in range(3)]
    m = Message("foo", *args)
    assert m.name == "foo"
    assert m.args[0].name == "0"
    assert m.args[1].name == "1"
    assert m.args[2].name == "2"


def test_next_prev(mio):
    m = Message("foo")
    m.next = Message("bar")

    assert m.prev == None
    assert m.name == "foo"
    assert m.next.name == "bar"
    assert m.next.next == None
    assert m.next.prev.name == "foo"
