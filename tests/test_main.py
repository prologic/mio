import os
import sys
from subprocess import Popen, PIPE

import main_wrapper

TEST_FILE = os.path.join(os.path.dirname(__file__), "test.mio")


def test_eval():
    p = Popen([sys.executable, main_wrapper.__file__, "-e", "(1 + 2) print"], stdout=PIPE)
    stdout = p.communicate()[0]
    assert stdout == "3"


def test_interactive():
    p = Popen([sys.executable, main_wrapper.__file__, "-i", TEST_FILE], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate("exit\n")[0]
    assert stdout.split()[0] == "3"


def test_repl():
    p = Popen([sys.executable, main_wrapper.__file__], stdin=PIPE, stdout=PIPE)
    stdout = p.communicate("(1 + 2) println\nexit\n")[0]
    assert stdout.split()[3] == "3"
