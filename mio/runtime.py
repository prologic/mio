"""runtime

...
"""

from os import path


from pkg_resources import resource_filename, resource_listdir


root = None
state = None


def init(args=None, opts=None, reinit=False):
    global root, state

    from state import State
    from object import Object

    root = Object()
    state = State(args, opts, root)
    state.create_objects()

    if opts is None or (opts is not None and not opts.nosys):
        for resource in resource_listdir(__package__, "lib"):
            filename = resource_filename(__package__, path.join("lib", resource))
            state.load(filename)


def find(name):
    global root
    return root[name]
