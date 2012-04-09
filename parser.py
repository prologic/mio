# -*- coding: utf-8 -*-

import re

from funcparserlib import Spec
from funcparserlib import make_comment, make_multiline_comment, make_tokenizer

from funcparserlib import ebnf_grammar, name_parser_vars
from funcparserlib import a, eof, fwd, many, maybe, op_, sometok, skip

from message import Message

regexps = {
    'escaped': ur'''
        \\                                  # Escape
          ((?P<standard>["\\/bfnrt])        # Standard escapes
        | (u(?P<unicode>[0-9A-Fa-f]{4})))   # uXXXX
        ''',
    'unescaped': ur'''
        [\x20-\x21\x23-\x5b\x5d-\uffff]     # Unescaped: avoid ["\\]
        ''',
}
re_esc = re.compile(regexps['escaped'], re.VERBOSE)


def tokenize(str):
    'str -> Sequence(Token)'
    specs = [
        make_multiline_comment(r'"""', r'"""'),
        make_comment(r'#'),
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


def make_id(n):
    return str(n)


def make_number(n):
    try:
        return int(n)
    except ValueError:
        return float(n)


def unescape(s):
    std = {
        '"': '"', '\\': '\\', '/': '/', 'b': '\b', 'f': '\f', 'n': '\n',
        'r': '\r', 't': '\t',
    }

    def sub(m):
        if m.group('standard') is not None:
            return std[m.group('standard')]
        else:
            return unichr(int(m.group('unicode'), 16))
    return re_esc.sub(sub, s)


def make_string(n):
    return unescape(n[1:-1])


def make_arguments(n):
    if n is None:
        return []
    else:
        return [n[0]] + n[1]


def make_message(n):
    return Message(n[0], n[1])

id = sometok("name") >> make_id
number = sometok("number") >> make_number
string = sometok("string") >> make_string

symbol = id | number | string

terminator = a("eof") | a("newline") | op_(";")

exp = fwd()

arguments = (
    op_("(") +
    maybe(exp + many(op_(",") + exp)) +
    op_(")")
    >> make_arguments)

message = (symbol + maybe(arguments)) >> make_message

exp_list = many(message | terminator)

exp.define(exp_list + skip(eof))

name_parser_vars(locals())


def parse(seq):
    'Sequence(Token) -> object'
    return exp.parse(seq)
