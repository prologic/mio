from mio.version import version


def test_args(mio):
    assert mio.eval("System args") == []


def test_version(mio):
    assert mio.eval("System version") == version


def test_exit(mio):
    try:
        mio.eval("System exit()")
        assert False
    except SystemExit as e:
        assert e.args[0] == 0


def test_exit_status(mio):
    try:
        mio.eval("System exit(1)")
        assert False
    except SystemExit as e:
        assert e.args[0] == 1
