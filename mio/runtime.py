lobby = None
state = None


def init(opts=None, reinit=False):
    global lobby, state

    from state import State
    from object import Object

    lobby = Object()
    state = State(opts, lobby)
    state.create_objects()


def find(name):
    global lobby
    return lobby[name]
