from pytest import raises


from mio.errors import AttributeError


def test_block(mio):
    mio.eval("x = block(1)")
    assert mio.eval("x()") == 1


def test_block_body(mio):
    mio.eval("x = block(1)")
    body = mio.eval("x body")
    assert body == mio.eval("Parser parse(\"1\")")


def test_block_scope(mio):
    try:
        mio.eval("n = 1")
        mio.eval("x = block(n)")
        assert mio.eval("x()") == 1
    finally:
        mio.eval("del(\"n\")")


def test_block_scope2(mio):
    mio.eval("Foo = Object clone()")
    mio.eval("Foo n = 1")
    mio.eval("Foo x = block(n)")
    with raises(AttributeError):
        assert mio.eval("Foo x()", reraise=True)


def test_block_get_args(mio):
    mio.eval("x = block(x, y, z, x + y + z)")
    assert mio.eval("x args") == ["x", "y", "z"]


def test_block_get_kwargs(mio):
    mio.eval("x = block(a=1, b=2, c=3, a * b * c)")
    assert mio.eval("x kwargs") == {"a": 1, "b": 2, "c": 3}


def test_block_args(mio):
    mio.eval("x = block(n, n)")
    assert mio.eval("x(1)") == 1


def test_block_star_args(mio):
    mio.eval("x = block(*args, args)")
    assert mio.eval("x(1, 2, 3)") == [1, 2, 3]


def test_block_kwargs(mio):
    mio.eval("x = block(n=1, n)")
    assert mio.eval("x()") == 1
    assert mio.eval("x(n=2)") == 2


def test_block_star_star_kwargs(mio):
    mio.eval("x = block(**kwargs, kwargs)")
    assert mio.eval("x(a=1, b=2, c=3)") == {"a": 1, "b": 2, "c": 3}


def test_block_args_kwargs(mio):
    mio.eval("x = block(x, y, z, a=1, b=2, c=3, (x + y + z) * (a + b + c))")
    assert mio.eval("x(1, 2, 3)") == 36
    assert mio.eval("x(1, 2, 3, a=0)") == 30


def test_block_repr(mio):
    mio.eval("x = block(1)")
    assert repr(mio.eval("x")) == "block()"


def test_block_repr_args(mio):
    mio.eval("x = block(n=1, n)")
    assert repr(mio.eval("x")) == "block(n=1)"


def test_block_repr_star_args(mio):
    mio.eval("x = block(*args, args)")
    assert repr(mio.eval("x")) == "block(*args)"


def test_block_repr_kwargs(mio):
    mio.eval("x = block(a=1, b=2, c=3, a + b + c))")
    assert repr(mio.eval("x")) == "block(a=1, b=2, c=3)"


def test_block_repr_star_kwargs(mio):
    mio.eval("x = block(**kwargs, kwargs)")
    assert repr(mio.eval("x")) == "block(**kwargs)"


def test_block_repr_args_kwargs(mio):
    mio.eval("x = block(x, y, z, a=1, b=2, c=3, (x + y + z) * (a + b + c))")
    assert repr(mio.eval("x")) == "block(x, y, z, a=1, b=2, c=3)"


def test_block_repr_star_args_kwargs(mio):
    mio.eval("x = block(*args, a=1, b=2, c=3, (a + b + c))")
    assert repr(mio.eval("x")) == "block(*args, a=1, b=2, c=3)"


def test_block_repr_star_args_star_star_kwargs(mio):
    mio.eval("x = block(*args, **kwargs, args; kwargs)")
    assert repr(mio.eval("x")) == "block(*args, **kwargs)"


def test_block_call(mio):
    x = mio.eval("""x = block("foo")""")
    assert mio.eval("x") == x
    assert mio.eval("x()") == "foo"
