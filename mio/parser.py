# -*- coding: utf-8 -*-

from operator import add

from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

from .message import Message


tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))


def tokenize(str):

    operators = r"(\*\*)|(==)|(<=)|(>=)|(\+=)|(-=)|(\*=)|(/=)|[+]|[-]|[*]|[/]|[=]|[<]|[>]"

    specs = [
        Spec("comment",    r'#.*'),
        Spec('whitespace', r'[ \t]+'),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)'),
        Spec('name',       r'%s' % operators),
        Spec('name',       r'[A-Za-z][A-Za-z0-9_]*'),
        Spec('op',         r'[\(\),\n;]'),
    ]
    useless = ['comment', 'whitespace']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def make_arguments(n):
    return (n[0],) + tuple(n[1])


def make_message(n):
    if isinstance(n, Token):
        return Message(n.value)

    name, args = n
    args = tuple(args) if args is not None else ()
    return Message(name, *args)


def make_chain(messages):
    if messages:
        reduce(add, messages)
        return messages[0]

    return Message("None")


identifier = sometok("name")
number = sometok("number")
string = sometok("string")

exp = fwd()
message = fwd()
arguments = fwd()
symbol = fwd()
terminator = fwd()

exp.define((
    many(message | terminator)) >> make_chain)

message.define((
    symbol +
    maybe(arguments)) >> make_message)

arguments.define((
    skip(op_("(")) +
    maybe(exp + maybe(many(skip(op_(",")) + exp))) +
    skip(op_(")"))) >> make_arguments)

symbol.define(identifier | number | string)

terminator.define((
    op("\n") | op(";")) >> make_message)


parse = exp.parse
