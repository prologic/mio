#!/usr/bin/python -i

from mio import parser
from mio import runtime


class FakeOpts(object):

    def __init__(self, **kwargs):
        super(FakeOpts, self).__init__()

        self.__dict__.update(**kwargs)


runtime.init(opts=FakeOpts(nosys=True))
eval = runtime.state.eval


def parse(s):
    return parser.parse(parser.tokenize(s))
