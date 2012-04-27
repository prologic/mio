# -*- coding: utf-8 -*-

import re
from decimal import Decimal
from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

from message import Message

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))

operators = [
    "**", "++", "--", "+=", "-=", "*=", "/=", "<<", ">>",
    "==", "!=", "<=", ">=",
    "+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "^", "&",
    "or", "and", "not", "return",
]


def is_op(s):
    return s in operators


def tokenize(str):

    ops = "|".join([re.escape(op) for op in operators])

    specs = [
        Spec("comment",    r'#.*'),
        Spec('whitespace', r'[ \t]+'),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?([0-9]+(\.[0-9]*)?)'),
        Spec('name',       ops),
        Spec('name',       r'[A-Za-z_][A-Za-z0-9_]*'),
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

    if len(n) == 2:
        name, args = n
    else:
        name, args = "", n

    args = tuple(args) if args is not None else ()
    return Message(name, *args)


def make_chain(messages):
    if not messages:
        return Message("")

    key, value = None, None
    root, prev = None, None

    while True:
        if len(messages) > 1 and messages[1].name == "=":
            key = messages.pop(0)
            op = messages.pop(0)
            if op.args:
                value = Message("", *op.args)
            else:
                value = messages.pop(0)
        elif value is not None:
            if messages and not messages[0].terminator:
                value.next = messages.pop(0)
            else:
                args = key, value
                key, value = None, None
                message = Message("set", *args)

                if root is None:
                    root = prev = message
                else:
                    prev.next = prev = message
        elif messages and is_op(messages[0].name):
            prev.next = prev = messages.pop(0)
            if messages:
                message = messages.pop(0)
                prev.args = (message,)
        elif messages:
            message = messages.pop(0)
            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
        else:
            break

    return root


def make_number(n):
    return Decimal(n)


string = sometok("string")
identifier = sometok("name")
number = sometok("number") >> make_number

exp = fwd()
message = fwd()
arguments = fwd()
symbol = fwd()
terminator = fwd()

exp.define((
    many(message | terminator)) >> make_chain)

message.define((
    (symbol +
    maybe(arguments)) | arguments) >> make_message)

arguments.define((
    skip(op_("(")) +
    maybe(exp + maybe(many(skip(op_(",")) + exp))) +
    skip(op_(")"))) >> make_arguments)

symbol.define(identifier | number | string)

terminator.define((
    op("\n") | op(";")) >> make_message)

parse = exp.parse
