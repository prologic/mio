lobby = None
state = None


def init(reinit=False):
    global lobby, state

    from state import State
    from object import Object

    lobby = Object()
    state = State(lobby)
    state.create_objects()


def find(name):
    global lobby
    return lobby.attrs[name]
