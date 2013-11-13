from pytest import fixture


from mio import runtime


@fixture(scope="session")
def mio(request):
    runtime.init()
    return runtime.state


def test_closure(mio, capfd):
    mio.eval("""
        foo = block(
            block(
                print("foo")
            )
        )
    """)

    mio.eval("x = foo()")
    assert mio.frommio(mio.eval("x()")) is None
    out, err = capfd.readouterr()
    assert out == "foo\n"


def test_closure_locals(mio):
    mio.eval("""
        counter = block(n,
            block(
                this n = n + 1
                n
            )
        )
    """)

    mio.eval("x = counter(1)")
    mio.eval("y = counter(2)")

    assert mio.eval("x()") == 2
    assert mio.eval("y()") == 3
    assert mio.eval("x()") == 3
    assert mio.eval("y()") == 4


def test_closure_locals2(mio):
    mio.eval("""
        counter = block(n,
            block(
                n = n + 1
                n
            )
        )
    """)

    mio.eval("x = counter(1)")

    assert mio.eval("x()") == 2
    assert mio.eval("x()") == 2
