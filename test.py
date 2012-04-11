#!/usr/bin/python -i

from functools import update_wrapper

from mio.object import Object

class Method(object):

    def __init__(self, name=None):
        super(Method, self).__init__()

        self.name = name

    def __call__(self, f):
        def wrapper(sender, receiver, context, *args):
            self.receiver = receiver
            self.context = context

            return f(sender, *args)

        wrapper.method = True

        return update_wrapper(wrapper, f)

    def __repr__(self):
        return "method(...)"

method = Method

class Foo(Object):

    @method()
    def foo(self, a, b):
        print(self.receiver, self.context)
        print(a, b)

foo = Foo()
