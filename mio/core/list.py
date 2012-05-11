from mio import runtime
from mio.utils import method

from mio.object import Object

from number import Number


class List(Object):

    def __init__(self, value=[]):
        super(List, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        return iter(self.value)

    def __str__(self):
        return "[%s]" % ", ".join([repr(x) for x in self.value])

    @method()
    def init(self, env, *args):
        self.value = list(args)

    # General Operations

    @method()
    def append(self, env, item):
        env.target.value.append(item)
        return env.target

    @method()
    def count(self, env, value):
        return Number(env.target.value.count(value))

    @method()
    def extend(self, env, *args):
        env.target.value.extend(args)
        return env.target

    @method()
    def len(self):
        return Number(len(env.target.value))

    @method()
    def at(self, env, index):
        return env.target.value[index]

    @method()
    def reverse(self, env):
        env.target.value.reverse()
        return env.target

    @method()
    def reversed(self, env):
        return self.clone(reversed(env.target.value))

    @method()
    def sort(self, env):
        env.target.value.sort()
        return env.target

    @method()
    def sorted(self, env):
        return self.clone(sorted(env.target.value))
