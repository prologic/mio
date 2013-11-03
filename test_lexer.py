#!/usr/bin/python -i

from operator import attrgetter


from mio import lexer


def tokenize(code):
    return " ".join(map(attrgetter("value"), lexer.tokenize(code)))
