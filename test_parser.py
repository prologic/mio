#!/usr/bin/python -i

import sys


from mio import lexer
from mio import parser
from mio import runtime
from mio.main import parse_args


opts, args = parse_args(sys.argv)
runtime.init(args, opts)
eval = runtime.state.eval


def parse(s):
    return parser.parse(lexer.tokenize(s))
