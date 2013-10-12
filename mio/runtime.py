"""runtime

...
"""

from os import path


from pkg_resources import resource_filename, resource_listdir


lobby = None
state = None


def init(args=None, opts=None, reinit=False):
    global lobby, state

    from state import State
    from object import Object

    lobby = Object()
    state = State(args, opts, lobby)
    state.create_objects()

    for resource in resource_listdir(__package__, "lib"):
        filename = resource_filename(__package__, path.join("lib", resource))
        state.load(filename)


def find(name):
    global lobby
    return lobby[name]
