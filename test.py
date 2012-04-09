#!/usr/bin/python -i

from bootstrap import Lobby
from parser import parse, tokenize


def eval(s):
    tokens = tokenize(s)
    print tokens
    return parse(tokens)
