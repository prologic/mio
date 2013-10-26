def test_closure(mio, capfd):
    mio.eval("""
        foo = method(
            return method(
                print("foo")
            )
        )
    """)

    mio.eval("x = foo()")
    assert mio.eval("x()").value is None
    out, err = capfd.readouterr()
    assert out == "foo\n"


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

    assert mio.eval("x()") == 2
    assert mio.eval("y()") == 3


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

    assert mio.eval("x()") == 2
    assert mio.eval("x()") == 2
