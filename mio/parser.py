# -*- coding: utf-8 -*-

from operator import add

from funcparserlib.lexer import make_tokenizer, Token

from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some

from message import Message


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

    name, args = n
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
    if messages:
        messages = reshuffle(messages)

        eq = Message("=")
        if eq in messages:
            index = messages.index(eq)
            key, value = messages[:index], messages[(index + 1):]

            if len(key) > 1:
                obj = key[:-1]
                key = key[-1:]
                reduce(add, obj)
                reduce(add, key)
                args = key[0], value[0]
                obj[0].next = Message("set_slot", *args)
                return obj[0]

            reduce(add, key)
            reduce(add, value)
            args = key[0], value[0]
            return Message("set_slot", *args)

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
