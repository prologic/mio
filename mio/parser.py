# -*- coding: utf-8 -*-

from __future__ import print_function


from funcparserlib.lexer import Token
from funcparserlib.parser import forward_decl as fwd
from funcparserlib.parser import a, many, maybe, skip, some


from mio import runtime
from mio.lexer import operators
from mio.core.message import Message

tokval = lambda tok: tok.value
sometok = lambda type: (some(lambda t: t.type == type) >> tokval)
op = lambda name: a(Token('op', name))
op_ = lambda name: skip(op(name))
Spec = lambda name, value: (name, (value,))


def make_arguments(n):
    opening, expression, expressions, closing = n
    arguments = [] if expression is None else [expression]
    arguments.extend(expressions)
    return (opening, arguments, closing)


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
        message = Message(name, value)
        message.next = Message(next, None, args)
    else:
        message = Message(name, value, args)

    return message


def is_assignment(message):
    return message.name == "="


def is_operator(message):
    return message.name in operators


def reshuffle(ms):
    r = []

    while ms:
        #x is not None --> not x is None
        if len(ms) > 1 and ms[0].name == "is" and ms[1].name == "not":
            r = r[:-1] + [ms[1], r[-1], ms[0]]
            ms = ms[2:]
            continue
        r.append(ms.pop(0))

    return r


def make_chain(messages, all=True):
    root = node = None

    while messages:
        if len(messages) > 1 and is_assignment(messages[1]):
            name = messages.pop(0).name
            object = runtime.find("String").clone(name)
            key = Message(name, object)

            op = messages.pop(0)

            if op.name == "=" and op.next is not None and op.next.name in ("()", "[]", "{}",):
                value = Message("()", args=[Message(op.next.name, args=op.next.args)])
            elif op.args:
                value = Message("()", args=op.args)
            else:
                value = make_chain(messages, all=False)

            message = Message("set", args=[key, value])
        elif is_operator(messages[0]):
            message = messages.pop(0)
            if messages and not message.args:
                if operators.get(message.name) == 1:
                    arg = messages.pop(0)
                    # Set the argument (a Message) previous attribute to the current message
                    arg.previous = message
                    message.args.append(arg)
                    message.call = True
                else:
                    chain = make_chain(messages, all=False)
                    if chain is not None:
                        # Set the argument (a Message) previous attribute to the current message
                        chain.previous = message
                        message.args.append(chain)
                        message.call = True
        elif messages[0].terminator and not all:
            break
        else:
            message = messages.pop(0)

        if root is None:
            root = node = message
        else:
            node.next = node = message

    return root


def make_expression(messages):
    return make_chain(reshuffle(messages))


def make_number(n):
    return runtime.find("Number").clone(n)


def make_string(n):
    if n and n[0] in "bu":
        prefix = n[0]
        n = n[1:]
    else:
        prefix = "u"

    if len(n) > 3 and (n[:3] in ("'''", '"""')):
        n = n[3:-3]
    else:
        n = n[1:-1]

    if prefix == "u":
        s = n.decode("unicode-escape")
    else:
        s = n.decode("string-escape")

    return runtime.find("String" if prefix == "u" else "Bytes").clone(s)


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
    many(message | terminator)) >> make_expression)

message.define(((symbol + maybe(arguments)) | arguments) >> make_message)

paren_arguments = op("(") + maybe(expression) + many(skip(op_(",")) + expression) + op(")")
bracket_arguments = op("[") + maybe(expression) + many(skip(op_(",")) + expression) + op("]")
brace_arguments = op("{") + maybe(expression) + many(skip(op_(",")) + expression) + op("}")
arguments.define((paren_arguments | bracket_arguments | brace_arguments) >> make_arguments)

symbol.define(identifier | number | operator | string)

parse = expression.parse
