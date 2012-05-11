from mio import runtime
from mio.utils import method

from mio.object import Object


from list import List


class Map(Object):

    def __init__(self, value={}):
        super(Map, self).__init__(value=value)

        self.create_methods()
        self["parent"] = runtime.state.find("Object")

    def __iter__(self):
        for item in self.value.items():
            yield List(item)

    def __str__(self):
        pairs = ", ".join(["%s: %r" % (k, v) for k, v in self.value.items()])
        return "{%s}" % pairs

    @method()
    def init(self, env, *args):
        it = iter(args)
        env.target.value = dict(zip(it, it))

    # General Operations

    @method()
    def clear(self, env):
        env.target.value.clear()
        return runtime.state.find("None")

    @method()
    def copy(self, env):
        return self.clone(env.target.value.copy())

    @method()
    def get(self, env, key, default=None):
        default = default if default else runtime.state.find("None")
        return env.target.value.get(key, default)

    @method()
    def has(self, env, key):
        if key in env.target.value:
            return runtime.state.find("True")
        return runtime.state.find("False")

    @method()
    def items(self, env):
        items = [List(item) for item in env.target.value.items()]
        return List(items)

    @method()
    def keys(self, env):
        return List(env.target.value.keys())

    @method()
    def set(self, env, key, value):
        env.target.value[key] = value
        return env.target

    @method()
    def values(self, env):
        return List(env.target.value.values())
