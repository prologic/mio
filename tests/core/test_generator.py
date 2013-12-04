from pytest import raises


from mio.errors import StopIteration


def test_generator(mio):
    mio.eval("""foo = block(
        yield 1
        yield 2
        yield 3
    )""")

    mio.eval("f = foo()")
    assert mio.eval("next(f)") == 1
    assert mio.eval("next(f)") == 2
    assert mio.eval("next(f)") == 3

    with raises(StopIteration):
        mio.eval("next(f)", reraise=True)
