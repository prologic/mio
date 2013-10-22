def test_closure(mio):
    mio.eval("""
        foo = method(
            return method(
                "foo" println
            )
        )
    """)

    mio.eval("x = foo")
    assert mio.eval("x") == "foo"


def test_closure_locals(mio):
    mio.eval("""
        counter = method(n,
            return block(
                self n = n + 1
                return n
            )
        )
    """)

    mio.eval("x = counter(1)")
    mio.eval("y = counter(2)")

    assert mio.eval("x") == 2
    assert mio.eval("y") == 3


def test_closure_locals2(mio):
    mio.eval("""
        counter = method(n,
            return block(
                n = n + 1
                return n
            )
        )
    """)

    mio.eval("x = counter(1)")

    assert mio.eval("x") == 2
    assert mio.eval("x") == 2
