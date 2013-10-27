from mio.types.number import Number
from mio.types.string import String
from mio.parser import parse, tokenize


def test_empty_message():
    assert parse(tokenize("")) is None


def test_parens():
    chain = parse(tokenize("(1)"))
    assert chain.name == "()"
    assert chain.args[0] == Number(1)


def test_parens2():
    chain = parse(tokenize("x(1)"))
    assert chain.name == "x"
    assert chain.args[0] == Number(1)


def test_parens3():
    chain = parse(tokenize("x = (1)"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0] == Number(1)


def test_brackets():
    chain = parse(tokenize("[1]"))
    assert chain.name == "[]"
    assert chain.args[0] == Number(1)


def test_brackets2():
    chain = parse(tokenize("x[1]"))
    assert chain.name == "x"
    assert chain.next.name == "[]"
    assert chain.next.args[0] == Number(1)


def test_brackets3():
    chain = parse(tokenize("x = [1]"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0].name == "[]"
    assert chain.args[1].args[0].args[0] == Number(1)


def test_braces():
    chain = parse(tokenize("{1}"))
    assert chain.name == "{}"
    assert chain.args[0] == Number(1)


def test_braces2():
    chain = parse(tokenize("x{1}"))
    assert chain.name == "x"
    assert chain.next.name == "{}"
    assert chain.next.args[0] == Number(1)


def test_braces3():
    chain = parse(tokenize("x = {1}"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0].name == "{}"
    assert chain.args[1].args[0].args[0] == Number(1)


def test_number_message():
    chain = parse(tokenize("1"))
    assert chain.name == Number(1)


def test_string_message():
    chain = parse(tokenize("\"foo\""))
    assert chain.name == String("foo")


def test_string_newline():
    chain = parse(tokenize(r'"\n"'))
    assert chain.name == "\n"


def test_simple_assignment():
    chain = parse(tokenize("x = 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == Number(1)


def test_multi_assignment():
    chain = parse(tokenize("x = 1\ny = 2"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == Number(1)
    assert chain.next.name == "\n"
    assert chain.next.next.name == "set"
    assert chain.next.next.args[0].name == "y"
    assert chain.next.next.args[1].name == Number(2)


def test_grouped_assignment():
    chain = parse(tokenize("x = (1)"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "()"
    assert chain.args[1].args[0] == Number(1)


def test_complex_assignment():
    chain = parse(tokenize("Foo x = 1"))
    assert chain.name == "Foo"
    assert chain.next.name == "set"
    assert chain.next.args[0].name == "x"
    assert chain.next.args[1].name == Number(1)


def test_complex_assignment2():
    chain = parse(tokenize("x = x + 1"))
    assert chain.name == "set"
    assert chain.args[0].name == "x"
    assert chain.args[1].name == "x"
    assert chain.args[1].next.name == "+"
    assert chain.args[1].next.args[0].name == Number(1)


def test_chaining():
    chain = parse(tokenize("Foo bar"))
    assert chain.name == "Foo"
    assert chain.next.name == "bar"


def test_operators():
    chain = parse(tokenize("1 + 2"))
    assert repr(chain) == "1 +(2)"

    chain = parse(tokenize("1 + 2 * 3"))
    assert repr(chain) == "1 +(2 *(3))"


def test_operators2():
    chain = parse(tokenize("foo = method(\n1 +(1)\n)"))
    assert repr(chain) == "set(foo, method(\n 1 +(1) \n))"


def test_return():
    chain = parse(tokenize("foo = method(return 1)"))
    assert repr(chain) == "set(foo, method(return(1)))"


def test_return2():
    chain = parse(tokenize("foo = method(return 1 + 2)"))
    assert repr(chain) == "set(foo, method(return(1 +(2))))"


def test_grouping():
    chain = parse(tokenize("1 + (2 * 3)"))
    assert repr(chain) == "1 +(2 *(3))"


def test_parse(mio):
    chain = mio.eval("Parser parse(\"1 + 2\")")
    assert repr(chain) == "1 +(2)"
