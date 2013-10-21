#!/usr/bin/python -i

from mio import parser
from mio import runtime


runtime.init()
eval = runtime.state.eval


def parse(s):
    return parser.parse(parser.tokenize(s))
