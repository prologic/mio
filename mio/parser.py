# -*- coding: utf-8 -*-

import re
from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

import runtime
from object import Object
from message import Message
from utils import pymethod, Null

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))

operators = [
    "**", "++", "--", "+=", "-=", "*=", "/=", "<<", ">>",
    "==", "!=", "<=", ">=",
    "+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "^", "&",
    "is", "or", "and", "not", "return",
]


def is_op(s):
    return s in operators


def tokenize(str):

    ops = "|".join([re.escape(op) for op in operators])

    specs = [
        Spec("comment",    r'#.*'),
        Spec('whitespace', r'[ \t]+'),
        Spec("terminator", r'[\n\r;]'),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?([0-9]+(\.[0-9]*)?)'),
        Spec('name',       ops),
        Spec('name',       r'[A-Za-z_][A-Za-z0-9_]*'),
        Spec('op',         r'[(){}\[\],]'),
    ]
    useless = ['comment', 'whitespace']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def make_arguments(n):
    return (n[0],) + tuple(n[1])


def make_message(n):
    if len(n) == 2:
        name, args = n
    else:
        name, args = "", n

    args = tuple(args) if args is not None else ()

    if hasattr(name, "value"):
        value = name
        name = name.value
    else:
        value = None

    return Message(name, *args, value=value)


def make_chain(messages):
    if messages == []:
        return Message("")

    key, value = None, None
    root, prev = None, None

    while True:
        if len(messages) > 1 and messages[1].name == "=":
            key = messages.pop(0)
            key = Message(key.name,
                    value=runtime.find("String").clone(key.name))
            op = messages.pop(0)
            if op.args:
                value = Message("", *op.args)
            else:
                value = messages.pop(0)

            message = Message("set", key, value)

            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
        elif value is not None:
            if messages and not messages[0].terminator:
                if is_op(messages[0].name):
                    op = messages.pop(0)
                    if messages:
                        message = messages.pop(0)
                        op.args = (message,)
                    value.next = op
                    value = op
                else:
                    message = messages.pop(0)
                    value.next = message
                    value = message
            else:
                key, value = None, None
        elif messages and is_op(messages[0].name) and not messages[0].args:
            message = messages.pop(0)
            if root is None:
                root = prev = message
            else:
                prev.next = prev = message
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
    return runtime.find("Number").clone(n)


def make_string(n):
    return runtime.find("String").clone(eval(n))


def make_terminator(n):
    return Message(n)


identifier = sometok("name")
string = sometok("string") >> make_string
number = sometok("number") >> make_number
terminator = sometok("terminator") >> make_terminator

exp = fwd()
message = fwd()
arguments = fwd()
symbol = fwd()

exp.define((
    many(message | terminator)) >> make_chain)

message.define((
    (symbol +
    maybe(arguments)) | arguments) >> make_message)

opening = op_("(") | op_("{") | op_("[")
closing = op_(")") | op_("}") | op_("]")

arguments.define((
    skip(opening) +
    maybe(exp + maybe(many(skip(op_(",")) + exp))) +
    skip(closing)) >> make_arguments)

symbol.define(identifier | number | string)

parse = exp.parse


class Parser(Object):

    def __init__(self, value=Null):
        super(Parser, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    @pymethod()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
