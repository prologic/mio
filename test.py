#!/usr/bin/python -i

from functools import update_wrapper

from mio.object import Object

class Method(object):

    def __init__(self, f, name=None):
        super(Method, self).__init__()

        self.f = f
        self.name = name

    def __call__(*args):
        print(repr(args))
        #return self.f(*args)

    def __repr__(self):
        return "method(...)"

def method(name=None):
    def wrapper(f):
        f.method = True
        return f

    return wrapper

class Foo(Object):

    @method()
    def foo(self, a, b):
        #print(self.receiver, self.context)
        print(a, b)

foo = Foo()
