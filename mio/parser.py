# -*- coding: utf-8 -*-

import re
from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

import runtime
from object import Object
from message import Message
from utils import method, Null

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))

operators = [
    "**", "++", "--", "+=", "-=", "*=", "/=", "<<", ">>",
    "==", "!=", "<=", ">=",
    "+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "^", "&", "?",
    "is", "or", "and", "not", "return",
]


def tokenize(str):

    ops = "|".join([re.escape(op) for op in operators])

    specs = [
        Spec("comment",    r'#.*'),
        Spec("whitespace", r"[ \t]+"),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?([0-9]+(\.[0-9]*)?)'),
        Spec('operator',   ops),
        Spec('identifier', r'[A-Za-z_][A-Za-z0-9_]*'),
        Spec('op',         r'[(){}\[\],:;\n\r]'),
    ]
    useless = ["comment", "whitespace"]
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def make_arguments(n):
    return (n[0], (n[1][0],) + tuple(n[1][1]), n[2])


def make_message(n):
    if len(n) == 2:
        if n[1] is not None and getattr(n[1][0], "type") == "op":
            if n[1][0].value == "(":
                name = n[0]  # Message arguments i.e: foo(1, 2, 3)
            elif n[1][0].value == "[":
                name = (n[0], "[]")
            elif n[1][0].value == "{":
                name = (n[0], "{}")
            args = n[1][1]
        else:
            name, args = n
    else:
        if n[0].value == "(":
            name = "()"
        elif n[0].value == "[":
            name = "[]"
        elif n[0].value == "{":
            name = "{}"
        args = n[1]

    args = tuple(args) if args is not None else ()

    if isinstance(name, tuple):
        name, next = name
    else:
        next = None

    if hasattr(name, "value"):
        value = name
        name = name.value
    else:
        value = None

    if next is not None:
        message = Message(name, value=value)
        message.next = Message(next, *args, value=next)
    else:
        message = Message(name, *args, value=value)

    return message


def is_assignment(message):
    return message.name == "="


def is_operator(message):
    return message.name in operators


def make_chain(messages, all=True):
    if messages == []:
        return Message("")

    root = node = None

    while messages:
        if len(messages) > 1 and is_assignment(messages[1]):
            name = messages.pop(0).name
            object = runtime.find("String").clone(name)
            key = Message(name, value=object)

            op = messages.pop(0)

            if op.name == "=" and op.next is not None and op.next.name in ("()", "[]", "{}",):
                value = Message("()", Message(op.next.name, *op.next.args))
            elif op.args:
                value = Message("()", *op.args)
            else:
                value = make_chain(messages, all=False)

            message = Message("set", key, value)
        elif is_operator(messages[0]):
            message = messages.pop(0)
            if messages:
                chain = make_chain(messages, all=False)
                if chain is not None:
                    # Set the argument (a Message) previous attribute to the current message
                    chain.previous = message
                    message.args.append(chain)
        elif messages[0].terminator and not all:
            break
        else:
            message = messages.pop(0)

        if root is None:
            root = node = message
        else:
            node.next = node = message

    return root


def make_number(n):
    return runtime.find("Number").clone(n)


def make_string(n):
    return runtime.find("String").clone(eval(n))


def make_terminator(n):
    return Message(n.value)


operator = sometok("operator")
identifier = sometok("identifier")
string = sometok("string") >> make_string
number = sometok("number") >> make_number

expression = fwd()
arguments = fwd()
message = fwd()
symbol = fwd()

terminator = (op(";") | op("\r") | op("\n")) >> make_terminator

expression.define((
    many(message | terminator)) >> make_chain)

message.define(((symbol + maybe(arguments)) | arguments) >> make_message)

opening = op("(") | op("{") | op("[")
closing = op(")") | op("}") | op("]")

paren_arguments = op("(") + maybe(expression + maybe(many(skip(op_(",")) + expression))) + op(")")
bracket_arguments = op("[") + maybe(expression + maybe(many(skip(op_(",")) + expression))) + op("]")
brace_arguments = op("{") + maybe(expression + maybe(many(skip(op_(",")) + expression))) + op("}")
arguments.define((paren_arguments | bracket_arguments | brace_arguments) >> make_arguments)

symbol.define(identifier | number | operator | string)

parse = expression.parse


class Parser(Object):

    def __init__(self, value=Null):
        super(Parser, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    @method()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
