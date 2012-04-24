
from mio.parser import parse, tokenize

tests = [
        ("1 + 1", 2),
        ("1 + 2 * 3", 7),
        ("1 + 2 * 3 - 1", 6),
        ("1 * 578 + (1 - 1)*578", 578),
        ("1 + 2 < 3", False),
        ("1 + 2 * 3 > 5", True),
]


def pytest_generate_tests(metafunc):
    for test in tests:
        metafunc.addcall(funcargs={"test": test})


def test(test):
    code, expected = test
    assert eval(repr(parse(tokenize(code)))) == expected
