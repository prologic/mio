# -*- coding: utf-8 -*-


import re

from errors import SyntaxError


def pos_to_str(pos):
    """((int, int), (int, int)) -> str"""

    start, end = pos
    sl, sp = start
    el, ep = end

    return "%d,%d-%d,%d" % (sl, sp, el, ep)


class Token(object):

    __slots__ = ["type", "value", "pos"]

    def __init__(self, type, value, pos=None):
        self.type = type
        self.value = value
        self.pos = pos

    def __repr__(self):
        return "Token(%r, %r)" % (self.type, self.value)

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False

        return (self.type == other.type and
                (self.value is None or
                 other.value is None or
                 self.value == other.value))

    def __hash__(self):
        return hash(self.type) ^ hash(self.value) ^ hash(self.pos)

    def __unicode__(self):
        return (u"%s %r" % (self.type, self.value)
                if self.value is not None
                else self.type)

    def __str__(self):
        return unicode(self).encode()

    def pformat(self):
        return u"%s %s %r" % (pos_to_str(self.pos).ljust(20),
            self.type.ljust(14), self.value)

    @property
    def name(self):
        return self.value


class Spec(object):

    def __init__(self, type, regexp, flags=0):
        self.type = type
        self._regexp = regexp
        self._flags = flags
        self.re = re.compile(regexp, flags)

    def __repr__(self):
        return "Spec(%r, %r, %r)" % (self.type, self._regexp, self._flags)


def make_tokenizer(specs):
    """[Spec] -> (str -> Iterable(Token))"""

    def tokenize(s):
        length = len(s)
        line, pos = 1, 0
        i = 0
        while i < length:
            for spec in specs:
                m = spec.re.match(s, i)
                if m is not None:
                    value = m.group()
                    nls = value.count("\n")
                    n_line = line + nls
                    value_len = len(value)
                    if nls == 0:
                        n_pos = pos + value_len
                    else:
                        n_pos = value_len - value.rfind("\n") - 1
                    yield Token(spec.type, value,
                                ((line, pos + 1), (n_line, n_pos)))
                    line, pos = n_line, n_pos
                    i += value_len
                    break
            else:
                errline = s.splitlines()[line - 1]
                raise SyntaxError(errline,
                        ((line, pos + 1), (line, len(errline))))

    return tokenize
