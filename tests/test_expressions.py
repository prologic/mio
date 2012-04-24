
from mio.parser import parse, tokenize

tests = [
        ("1 + 1", "1 +(1)"),
        ("1 + 2 * 3", "1 +(2 *(3))"),
        ("1 + 1 * 1 + 1", "1 +(1 *(1)) +(1)"),
]


def pytest_generate_tests(metafunc):
    for test in tests:
        metafunc.addcall(funcargs={"test": test})


def test(test):
    code, expected = test
    message = parse(tokenize(code))
    assert repr(message) == expected
