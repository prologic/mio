import sys

from mio import __version__


def test_args(mio):
    assert mio.eval("System args") == []


def test_version(mio):
    assert mio.eval("System version") == __version__


def test_stdin(mio):
    assert mio.eval("System stdin") == sys.stdin


def test_stdout(mio):
    assert mio.eval("System stdout") == sys.stdout


def test_stderr(mio):
    assert mio.eval("System stderr") == sys.stderr


def test_exit(mio):
    try:
        mio.eval("System exit")
        assert False
    except SystemExit as e:
        assert e.args[0] == 0


def test_exit_status(mio):
    try:
        mio.eval("System exit(1)")
        assert False
    except SystemExit as e:
        assert e.args[0] == 1
