from mio.parser import parse
from mio.lexer import tokenize
from mio.types.number import Number
from mio.types.string import String


def test_empty_message(mio):
    assert parse(tokenize("")) is None


def test_parens(mio):
    chain = parse(tokenize("(1)"))
    assert chain.name == "()"
    assert chain.args[0] == Number(1)


def test_parens2(mio):
    chain = parse(tokenize("x(1)"))
    assert chain.name == "x"
    assert chain.args[0] == Number(1)


def test_parens3(mio):
    chain = parse(tokenize("x = (1)"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0] == Number(1)


def test_brackets(mio):
    chain = parse(tokenize("[1]"))
    assert chain.name == "[]"
    assert chain.args[0] == Number(1)


def test_brackets2(mio):
    chain = parse(tokenize("x[1]"))
    assert chain.name == "x"
    assert chain.next.name == "[]"
    assert chain.next.args[0] == Number(1)


def test_brackets3(mio):
    chain = parse(tokenize("x = [1]"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0].name == "[]"
    assert chain.args[1].args[0].args[0] == Number(1)


def test_braces(mio):
    chain = parse(tokenize("{1}"))
    assert chain.name == "{}"
    assert chain.args[0] == Number(1)


def test_braces2(mio):
    chain = parse(tokenize("x{1}"))
    assert chain.name == "x"
    assert chain.next.name == "{}"
    assert chain.next.args[0] == Number(1)


def test_braces3(mio):
    chain = parse(tokenize("x = {1}"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0].name == "{}"
    assert chain.args[1].args[0].args[0] == Number(1)


def test_number_message(mio):
    chain = parse(tokenize("1"))
    assert chain.name == Number(1)


def test_string_message(mio):
    chain = parse(tokenize("\"foo\""))
    assert chain.name == String("foo")


def test_string_newline(mio):
    chain = parse(tokenize(r'"\n"'))
    assert chain.name == "\n"


def test_simple_assignment(mio):
    chain = parse(tokenize("x = 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == Number(1)


def test_multi_assignment(mio):
    chain = parse(tokenize("x = 1\ny = 2"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == Number(1)
    assert chain.next.name == "\n"
    assert chain.next.next.name == "set"
    assert chain.next.next.args[0].name == "y"
    assert chain.next.next.args[1].name == Number(2)


def test_grouped_assignment(mio):
    chain = parse(tokenize("x = (1)"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0] == Number(1)


def test_complex_assignment(mio):
    chain = parse(tokenize("Foo x = 1"))
    assert chain.name == "Foo"
    assert chain.next.name == "set"
    assert chain.next.args[0].name == "x"
    assert chain.next.args[1].name == Number(1)


def test_complex_assignment2(mio):
    chain = parse(tokenize("x = x + 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "x"
    assert chain.args[1].next.name == "+"
    assert chain.args[1].next.args[0].name == Number(1)


def test_chaining(mio):
    chain = parse(tokenize("Foo bar"))
    assert chain.name == "Foo"
    assert chain.next.name == "bar"


def test_operators(mio):
    chain = parse(tokenize("1 + 2"))
    assert repr(chain) == "1 +(2)"

    chain = parse(tokenize("1 + 2 * 3"))
    assert repr(chain) == "1 +(2) *(3)"


def test_operators_assignment(mio):
    chain = parse(tokenize("foo = method(\n1 +1\n)"))
    assert repr(chain) == "set(foo, method(\n 1 +(1) \n))"


def test_grouping(mio):
    chain = parse(tokenize("1 + (2 * 3)"))
    assert repr(chain) == "1 +(2 *(3))"


def test_parse(mio):
    chain = mio.eval("Parser parse(\"1 + 2\")")
    assert repr(chain) == "1 +(2)"


def test_reshuffle(mio):
    chain = parse(tokenize("x is not None"))
    assert repr(chain) == "not(x is(None))"
