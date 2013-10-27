"""runtime

...
"""

from os import path


from pkg_resources import resource_filename, resource_listdir


state = None


def init(args=[], opts=None):
    global state

    from state import State

    state = State(args, opts)
    state.create_objects()

    if opts is None or (opts is not None and not opts.nosys):
        for resource in resource_listdir(__package__, path.join("lib", "bootstrap")):
            filename = resource_filename(__package__, path.join("lib", "bootstrap", resource))
            state.load(filename)


def find(name):
    global state

    return state.find(name)
