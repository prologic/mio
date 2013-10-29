"""runtime

...
"""


state = None


def init(args=[], opts=None):
    global state

    from state import State

    state = State(args, opts)
    state.create_objects()


def find(name):
    global state

    return state.find(name)
