# -*- coding: utf-8 -*-

from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import a, many, maybe, skip, some, Parser
from funcparserlib.parser import finished as eof
from funcparserlib.parser import forward_decl as fwd

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))


def name_parser_vars(vars):
    """Name parsers after their variables.

    Named parsers are nice for debugging and error reporting.

    The typical usage is to define all the parsers of the grammar in
    the same scope and run `name_parser_vars(locals())` to name them
    all instead of calling `Parser.named()` manually for each parser.
    """

    for k, v in vars.items():
        if isinstance(v, Parser):
            v.named(k)

from message import Message


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        Spec("newline",       r'[\r\n]+'),
        Spec('whitespace',    r'[ \t]+'),
        Spec('string',        r'"[^"]*"'),
        Spec('number',        r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)'),
        Spec('name',          r'[A-Za-z][A-Za-z0-9_]*'),
        Spec('op',            r'[\(\)\[\]=+-/*;]'),
    ]
    useless = ['comment', 'whitespace']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def make_arguments(n):
    return [n[0]] + n[1]


def make_message(n):
    return Message(n[0], n[1])


def make_chain(xs):
    a = xs[0]
    for x in xs[1:]:
        a.next = x
        a = x
    return xs[0]


id = sometok("name")
number = sometok("number")
string = sometok("string")

symbol = id | number | string

terminator = sometok("newline") | op(";")

exp = fwd()

arguments = (
    op_("(") +
    maybe(exp + many(op_(",") + exp)) +
    op_(")")
    >> make_arguments)

message = (symbol + maybe(arguments)) >> make_message

exp_list = many(message + skip(many(terminator)))

exp.define((exp_list >> make_chain) + skip(eof))

name_parser_vars(locals())


def parse(seq):
    'Sequence(Token) -> object'
    return exp.parse(seq)
