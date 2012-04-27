from decimal import Decimal

from mio.parser import parse, tokenize


def test_simple_assignment():
    chain = parse(tokenize("x = 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == Decimal(1)


def test_complex_assignment():
    chain = parse(tokenize("Foo x = 1"))
    assert chain.name == "Foo"
    assert chain.next.name == "set"
    assert chain.next.args[0].name == "x"
    assert chain.next.args[1].name == Decimal(1)


def test_complex_assignment2():
    chain = parse(tokenize("x = x + 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "x"
    assert chain.args[1].next.name == "+"
    assert chain.args[1].next.args[0].name == Decimal("1")


def test_chaining():
    chain = parse(tokenize("Foo bar"))
    assert chain.name == "Foo"
    assert chain.next.name == "bar"


def test_operators():
    chain = parse(tokenize("1 + 2"))
    assert repr(chain) == "1 +(2)"

    chain = parse(tokenize("1 + 2 * 3"))
    assert repr(chain) == "1 +(2) *(3)"


def test_grouping():
    chain = parse(tokenize("1 + (2 * 3)"))
    assert repr(chain) == "1 +(2 *(3))"
