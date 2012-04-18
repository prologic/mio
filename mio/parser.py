# -*- coding: utf-8 -*-

from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

from message import Message

EQ = Message("=")

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))


def tokenize(str):

    sops = r"[+]|[-]|[*]|[/]|[=]|[<]|[>]"
    dops = r"(\*\*)|(==)|(<=)|(>=)|(\+=)|(-=)|(\*=)|(/=)"

    specs = [
        Spec("comment",    r'#.*'),
        Spec('whitespace', r'[ \t]+'),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?(\.[0-9]+)|([0-9]+(\.[0-9]*)?)'),
        Spec('name',       dops),
        Spec('name',       sops),
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

prec = {
        "**":  1,

        "*":   2,
        "/":   2,
        "%":   2,

        "+":   3,
        "-":   3,

        "<<":  4,
        ">>":  4,

        ">":   5,
        "<":   5,
        "<=":  5,
        ">=":  5,

        "==":  6,
        "!=":  6,

        "&":   7,

        "^":   8,

        "|":   9,

        "and": 10,
        "&&":  10,

        "or":  11,
        "||":  11,

        "..":  12,

        "+=":  13,
        "-=":  13,
        "*=":  13,
        "/=":  13,
        "%=":  13,
        "&=":  13,
        "^=":  13,
        "|=":  13,
        "<<=": 13,
        ">>=": 13,

        "return": 14,
}

right = {}


def getprec(op):
    return prec.get(op, -1)


def reshuffle(messages):
    ops = []
    output = []

    for message in messages:
        if len(message.args) == 0 and getprec(message.name) > 0:
            pr = getprec(message.name)
            if message.name in right:
                while ops and pr < getprec(ops[-1]):
                    output.append(ops.pop())
            else:
                while ops and pr <= getprec(ops[-1]):
                    output.append(ops.pop())

            ops.append(message)
        else:
            output.append(message)

    if not ops:
        return output

    ops.reverse()
    output.reverse()

    m = ops.pop()
    root = o = output.pop()

    prev = None
    while output:
        if prev is not None:
            prev.args = (o,)

        o.next = m
        prev = m

        if ops:
            m = ops.pop()

        o = output.pop()

    if prev is not None:
        prev.args = (o,)

    return [root]


def make_chain(messages):
    if not messages:
        return Message("")

    messages = list(reversed(reshuffle(messages)))

    key, value = None, None
    root, next = None, None

    while True:
        if len(messages) > 1 and messages[-2] == EQ:
            key = messages.pop()
            if messages[-1].args:
                value = Message("", *messages.pop().args)
            else:
                messages.pop()
                value = messages.pop()
        elif value is not None:
            if (not messages) or (messages and messages[-1].terminator):
                args = key, value
                key, value = None, None
                message = Message("set_slot", *args)
                if root is None:
                    root = next = message
                else:
                    next.next = next = message
            else:
                value.next = messages.pop()
        else:
            if messages:
                message = messages.pop()
            else:
                break

            if root is None:
                root = next = message
            else:
                next.next = next = message

    return root


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
