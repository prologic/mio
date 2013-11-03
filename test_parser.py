#!/usr/bin/python -i

from mio import lexer
from mio import parser
from mio import runtime


class FakeOpts(object):

    def __init__(self, **kwargs):
        super(FakeOpts, self).__init__()

        self.__dict__.update(**kwargs)

opts = FakeOpts(nosys=True)
runtime.init(opts=opts)
eval = runtime.state.eval


def parse(s):
    return parser.parse(lexer.tokenize(s))
