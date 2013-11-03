#!/usr/bin/env python


import re
from collections import OrderedDict


from funcparserlib.lexer import make_tokenizer, Token


tokval = lambda tok: tok.value
Spec = lambda name, value: (name, (value,))

operators = OrderedDict([
    ("**", (1, 15)), ("++", (1, 15)), ("--", (1, 15)), ("+=", (1, 0)), ("-=", (1, 0)), ("*=", (1, 0)), ("/=", (1, 0)),
    ("<<", (1, 10)), (">>", (1, 10)), ("==", (0, 6)), ("!=", (0, 6)), ("<=", (0, 6)), (">=", (0, 6)), ("..", (1, 0)),

    ("+", (1, 11)), ("-", (1, 11)), ("*", (1, 12)), ("/", (1, 12)), ("=", (1, 0)), ("<", (0, 6)), (">", (0, 6)),
    ("!", (0, 0)), ("%", (12, 1)), ("|", (0, 7)), ("^", (0, 8)), ("&", (0, 9)), ("?", (1, 0)), (":", (1, 0)),

    ("in", (0, 4)), ("is", (0, 5)), ("or", (0, 1)), ("and", (0, 2)), ("not", (0, 3)),

    ("return", (0, 0)), ("from", (1, 0)), ("import", (1, 0)), ("raise", (0, 0)),
])

strtpl = """
    {start:s}
    [^\\{quote:s}]*?
    (
    (   \\\\[\000-\377]
        |   {quote:s}
        (   \\\\[\000-\377]
        |   [^\\{quote:s}]
        |   {quote:s}
        (   \\\\[\000-\377]
            |   [^\\{quote:s}]
        )
        )
    )
    [^\\{quote:s}]*?
    )*?
    {end:s}
"""

quotes = [
    {"quote": "'", "start": "'''", "end": "'''"},
    {"quote": '"', "start": '"""', "end": '"""'},
    {"quote": "'", "start": "'", "end": "'"},
    {"quote": '"', "start": '"', "end": '"'}
]

strre = "".join(strtpl.split())
strre = "|".join([strre.format(**quote) for quote in quotes])
strre = re.compile(strre.format(**quotes[3]))

encodnig = "utf-8"


def findtoken(tokens, *args):
    for arg in args:
        try:
            return tokens.index(arg)
        except ValueError:
            pass


def getlevel(token):
    type = token.type
    value = token.value
    return operators.get(value, operators.get(type, (0, 0)))[1]


def isoperator(token):
    type = token.type
    value = token.value
    return type in operators or value in operators


def precedence(tokens):
    lparen = Token("op", "(")
    rparen = Token("op", ")")
    assign = Token("operator", "=")
    terminators = (Token("op", ";"), Token("op", "\r"), Token("op", "\n"),)

    level = None
    levels = []
    output = []

    while tokens:
        if tokens and tokens[0].value in ";\r\n":
            while len(levels) > 1:
                level = levels.pop()
                output.append(rparen)
            level = None
            levels = []
            output.append(tokens.pop(0))
        elif assign in tokens and (findtoken(tokens, *terminators) is None or findtoken(tokens, assign) < findtoken(tokens, *terminators)):
            i = findtoken(tokens, assign)
            e = findtoken(tokens, *terminators)

            if e is not None:
                lhs, rhs, rest = tokens[:i], tokens[(i + 1):(e + 1)], tokens[(e + 1):]
            else:
                lhs, rhs, rest = tokens[:i], tokens[(i + 1):], []

            output.extend(precedence(lhs))
            output.append(assign)
            output.extend(precedence(rhs))
            tokens = rest
            level = None
            levels = []
        elif tokens and tokens[0].value in "()":
            level = None
            levels = []
            output.append(tokens.pop(0))
        else:
            if len(tokens) > 1 and isoperator(tokens[1]):
                level = getlevel(tokens[1])

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


def tokenize(str):

    ops = "|".join([re.escape(op) for op in operators])

    specs = [
        Spec("comment",    r'#.*'),
        Spec("whitespace", r"[ \t]+"),
        Spec('string',     strre),
        Spec('number',     r'(-?(0|([1-9][0-9]*))(\.[0-9]+)?([Ee]-?[0-9]+)?)'),
        Spec('identifier', r'[A-Za-z_][A-Za-z0-9_]*'),
        Spec('operator',   ops),
        Spec('op',         r'[(){}\[\],:;\n\r]'),
    ]
    useless = ["comment", "whitespace"]
    t = make_tokenizer(specs)
    return precedence([x for x in t(str) if x.type not in useless])
