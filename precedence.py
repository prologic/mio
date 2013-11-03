#!/usr/bin/env python


from collections import OrderedDict


operators = OrderedDict([
    ("*", (2)), ("/", (2)),
    ("+", (1)), ("-", (1)),
])


def findtoken(tokens, *args):
    for arg in args:
        try:
            return tokens.index(arg)
        except ValueError:
            pass


def precedence(tokens):
    lparen = "("
    rparen = ")"

    level = None
    levels = []
    output = []

    while tokens:
        if tokens and tokens[0] in ";\r\n":
            while len(levels) > 1:
                level = levels.pop()
                output.append(rparen)
            level = None
            levels =[]
            output.append(tokens.pop(0))
        elif tokens and tokens[0] in "()":
            level = None
            levels = []
            output.append(tokens.pop(0))
        else:
            if len(tokens) > 1 and tokens[1] in operators:
                level = operators.get(tokens[1])

                if levels:
                    if level > levels[-1]:
                        levels.append(level)
                        output.append(lparen)
                else:
                    levels.append(level)

            output.append(tokens.pop(0))
            while levels and level < levels[-1]:
                level = levels.pop()
                output.append(rparen)

    while len(levels) > 1:
        level = levels.pop()
        output.append(rparen)

    return output


def parse(code):
    return code.split(" ")


def test1():
    tokens = parse("1 + 2")
    output = " ".join(precedence(tokens))
    assert output == "1 + 2"


def test2():
    tokens = parse("1 + 2 * 3")
    output = " ".join(precedence(tokens))
    assert output == "1 + ( 2 * 3 )"


def test3():
    tokens = parse("1 + 2 * 3 + 4")
    output = " ".join(precedence(tokens))
    assert output == "1 + ( 2 * 3 ) + 4"


def test4():
    tokens = parse("x = x + 1")
    output = " ".join(precedence(tokens))
    assert output == "x = x + 1"


def test5():
    tokens = parse("x = x + 1 + 2")
    output = " ".join(precedence(tokens))
    assert output == "x = x + 1 + 2"


def test6():
    tokens = parse("x = x + 1 + 2 * 3")
    output = " ".join(precedence(tokens))
    assert output == "x = x + 1 + ( 2 * 3 )"


def test7():
    tokens = parse("1 + ( 2 * 3 )")
    output = " ".join(precedence(tokens))
    assert output == "1 + ( 2 * 3 )"


def test8():
    tokens = parse("( 1 + 2 ) * 3")
    output = " ".join(precedence(tokens))
    assert output == "( 1 + 2 ) * 3"


def test9():
    tokens = parse("x = 1 + 2 * 3 ; y = 4")
    output = " ".join(precedence(tokens))
    assert output == "x = 1 + ( 2 * 3 ) ; y = 4"
