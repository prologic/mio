#!/usr/bin/python -i

from mio import runtime
runtime.init()

from mio.parser import parse, tokenize


def eval(s):
    return parse(tokenize(s))
