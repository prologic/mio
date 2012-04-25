# -*- coding: utf-8 -*-

from operator import add
from decimal import Decimal
from itertools import izip_longest
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

    sops = r"[+]|[-]|[*]|[/]|[=]|[<]|[>]|[!]"
    dops = r"(\*\*)|(==)|(!=)|(<=)|(>=)|(\+=)|(-=)|(\*=)|(/=)"

    specs = [
        Spec("comment",    r'#.*'),
        Spec('whitespace', r'[ \t]+'),
        Spec('string',     r'"[^"]*"'),
        Spec('number',     r'-?([0-9]+(\.[0-9]*)?)'),
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

        #TODO: "&":   7,

        #TODO: "^":   8,

        #TODO: "|":   9,

        "and": 10,
        "or":  11,

        #TODO: ...
        #"+=":  13,
        #"-=":  13,
        #"*=":  13,
        #"/=":  13,
        #"%=":  13,
        #"&=":  13,
        #"^=":  13,
        #"|=":  13,
        #"<<=": 13,
        #">>=": 13,

        #"return": 14,
}

right = {}


def getprec(op):
    return prec.get(op, -1)


def reshuffle(messages):
    ops = []
    msgs = []

    for message in messages:
        pr = getprec(message.name)
        if pr > 0:
            if message.name in right:
                while ops and pr < getprec(ops[-1]):
                    msgs.append(ops.pop())
            else:
                while ops and pr <= getprec(ops[-1]):
                    msgs.append(ops.pop())

            if message.args:
                # If this operator (message) has arguments then
                # split the operator from it's arguments.
                msgs.append(Message("", *message.args))
                message = Message(message.name)

            ops.append(message)
        else:
            msgs.append(message)

    if not ops:
        return msgs

    root = msgs[0]

    prev = None
    lpr, cpr = None, None
    for msg, op in izip_longest(msgs, ops):
        lpr = cpr
        cpr = getprec(op.name) if op is not None else None

        if lpr is None and cpr is None:
            x = root
            while x.next is not None:
                x = x.next
            x.next = msg
        elif lpr is not None:
            if cpr < lpr: # binds tighter?
                prev.args = (msg,)
                msg.next = op
                prev = op
            else:
                prev.args = (msg,)

                x = root
                while x.next is not None:
                    x = x.next
                x.next = op

                prev = op
        else:
            msg.next = op
            prev = op

    return [root]


def make_chain(messages):
    if not messages:
        return Message("")

    messages.reverse()

    results = []
    key, value = None, []

    while True:
        if len(messages) > 1 and messages[-2].name == "=":
            key = messages.pop()
            if messages[-1].args:
                value.append(Message("", *messages.pop().args))
            else:
                messages.pop()
                value.append(messages.pop())
        elif value:
            if (not messages) or (messages and messages[-1].terminator):
                value = reshuffle(value)
                reduce(add, value)
                args = key, value[0]
                key, value = None, []
                results.append(Message("set", *args))
            else:
                value.append(messages.pop())
        else:
            if not messages:
                break
            results.append(messages.pop())

    reduce(add, reshuffle(results))

    return results[0]


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
