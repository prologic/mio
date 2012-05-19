import os
from subprocess import Popen, PIPE


TEST_FILE = os.path.join(os.path.dirname(__file__), "test.mio")


def test_eval():
    p = Popen(["mio", "-e", "(1 + 2) print"], stdout=PIPE)
    stdout = p.communicate()[0]
    assert p.returncode == 0
    assert stdout == "3"


def test_interactive():
    p = Popen(["mio", "-i", TEST_FILE], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate("exit\n")[0]
    assert p.returncode == 0
    assert stdout.split("\n")[0] == "3"


def test_repl():
    p = Popen(["mio"], stdin=PIPE, stdout=PIPE)
    stdout  = p.communicate("(1 + 2) println\nexit\n")[0]
    assert p.returncode == 0
    assert stdout.split("\n")[1] == ">>> 3"