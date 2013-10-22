def test_method(mio):
    mio.eval("x = method(1)")
    assert mio.eval("x") == 1


def test_method_body(mio):
    mio.eval("x = method(1)")
    body = mio.eval("get(\"x\") body")
    assert body == mio.eval("Parser parse(\"1\")")


def test_method_scope(mio):
    mio.eval("Foo = Object clone")
    mio.eval("Foo n = 1")
    mio.eval("Foo x = method(n)")
    assert mio.eval("x") == 1


def test_method_get_args(mio):
    mio.eval("x = method(x, y, z, x + y + z)")
    assert mio.eval("get(\"x\") args") == ["x", "y", "z"]


def test_method_get_kwargs(mio):
    mio.eval("x = method(a=1, b=2, c=3, a * b * c)")
    assert mio.eval("get(\"x\") kwargs") == {"a": 1, "b": 2, "c": 3}


def test_method_args(mio):
    mio.eval("x = method(n, n)")
    assert mio.eval("x(1)") == 1


def test_method_kwargs(mio):
    mio.eval("x = method(n=1, n)")
    assert mio.eval("x") == 1
    assert mio.eval("x(n=2)") == 2


def test_method_args_kwargs(mio):
    mio.eval("x = method(x, y, z, a=1, b=2, c=3, (x + y + z) * (a + b + c))")
    assert mio.eval("x(1, 2, 3)") == 36
    assert mio.eval("x(1, 2, 3, a=0)") == 30


def test_method_repr(mio):
    mio.eval("x = method(1)")
    assert repr(mio.eval("get(\"x\")")) == "method()"


def test_method_repr_args(mio):
    mio.eval("x = method(n=1, n)")
    assert repr(mio.eval("get(\"x\")")) == "method(n=1)"


def test_method_repr_args_kwargs(mio):
    mio.eval("x = method(x, y, z, a=1, b=2, c=3, (x + y + z) * (a + b + c))")
    assert repr(mio.eval("get(\"x\")")) == "method(x, y, z, a=1, b=2, c=3)"
