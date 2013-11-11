"""runtime

...
"""


def init(args=[], opts=None):
    global state

    from state import State

    state = State(args, opts)
    state.bootstrap()
    state.initialize()


def find(name):
    global state

    return state.find(name)
