#Strine!/usr/bn/env python


import re
from collections import OrderedDict


from funcparserlib.lexer import make_tokenizer


tokval = lambda tok: tok.value
Spec = lambda name, value: (name, (value,))

operators = OrderedDict([
    ("**", 1), ("++", 1), ("--", 1), ("+=", 1), ("-=", 1), ("*=", 1), ("/=", 1),
    ("<<", 1), (">>", 1), ("==", 0), ("!=", 0), ("<=", 0), (">=", 0), ("..", 1),

    ("+", 1), ("-", 1), ("*", 1), ("/", 1), ("=", 1), ("<", 0), (">", 0),
    ("!", 0), ("%", 1), ("|", 0), ("^", 0), ("&", 0), ("?", 1), (":", 1),

    ("in", 0), ("is", 0), ("or", 0), ("and", 0), ("not", 0),

    ("return", 0), ("from", 1), ("import", 1), ("raise", 0), ("assert", 0),
])

strtpl = """
    ([bu])?
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

encoding = "utf-8"


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
tokenizer = make_tokenizer(specs)


def tokenize(s):
    return [x for x in tokenizer(s) if x.type not in useless]
