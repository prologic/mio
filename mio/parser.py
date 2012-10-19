# -*- coding: utf-8 -*-

import re
from itertools import izip

import runtime
from object import Object
from message import Message
from utils import pymethod, Null
from lexer import make_tokenizer, Spec


operators = [
    "**", "++", "--", "+=", "-=", "*=", "/=", "<<", ">>",
    "==", "!=", "<=", ">=",
    "+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "^", "&",
    "is", "or", "and", "not", "return"
]


def is_op(s):
    return s in operators


def tokenize(s):

    ops = "|".join([re.escape(op) for op in operators])

    specs = [
        Spec("comment",    r"#.*"),
        Spec("whitespace", r"[ \t]+"),
        Spec("terminator", r"[\n\r;]"),
        Spec("string",     r"\"[^\"]*\""),
        Spec("number",     r"-?([0-9]+(\.[0-9]*)?)"),
        Spec("name",       ops),
        Spec("name",       r"[A-Za-z_][A-Za-z0-9_]*"),
        Spec("op",         r"[(){}\[\],]"),
    ]
    useless = ["comment", "whitespace"]
    tokenizer = make_tokenizer(specs)
    return [x for x in tokenizer(s) if x.type not in useless]


def arguments(tokens):
    arg = None
    args = []

    while tokens:
        if tokens[0].type == "op" and tokens[0].value == ")":
            if arg is not None:
                args.append(arg)
            break
        elif tokens[0].type == "op" and tokens[0].value == ",":
            args.append(arg)
            arg = None
            tokens.pop(0)
        else:
            arg = expression(tokens)

    return args


def expression(tokens):
    if not tokens:
        return Message("")

    root, node = None, None

    while tokens:
        if tokens[0].type == "op" and tokens[0].value == ",":
            break
        elif tokens[0].type == "op" and tokens[0].value == ")":
            break
        elif tokens[0].type == "op" and tokens[0].value == "(":
            tokens.pop(0)
            args = arguments(tokens)
            if tokens[0].type == "op" and tokens[0].value == ")":
                if root is None:
                    node = root = Message("")

                if node.args:
                    node.next = node = Message("")

                node.args = args
                tokens.pop(0)
            else:
                raise SyntaxError("Invalid Syntax", tokens[0])
        elif len(tokens) > 1 and tokens[1].value == "=":
            message = Message("set")
            token = tokens.pop(0)
            object = runtime.find("String").clone(token.value)
            message.args.append(Message(token.value, value=object))
            tokens.pop(0)
            message.args.append(expression(tokens))

            if root is None:
                node = root = message
            else:
                node.next = node = message
        elif is_op(tokens[0].value):
            token = tokens.pop(0)
            message = Message(token.value)
            result = expression(tokens)
            if result.name == "" and len(result.args) == 1:
                message.args.append(result.args[0])
            else:
                message.args.append(result)

            if root is None:
                node = root = message
            else:
                node.next = node = message
        elif tokens[0].type == "number":
            token = tokens.pop(0)
            object = runtime.find("Number").clone(token.value)
            message = Message(object, value=object)
            if root is None:
                node = root = message
            else:
                node.next = node = message
        elif tokens[0].type == "string":
            token = tokens.pop(0)
            object = runtime.find("String").clone(eval(token.value))
            value = eval(token.value)
            message = Message(value, value=object)
            if root is None:
                node = root = message
            else:
                node.next = node = message
        else:
            token = tokens.pop(0)
            message = Message(token.value)
            if root is None:
                node = root = message
            else:
                node.next = node = message

    return root


parse = expression


class Parser(Object):

    def __init__(self, value=Null):
        super(Parser, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.state.find("Object")

    @pymethod()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
