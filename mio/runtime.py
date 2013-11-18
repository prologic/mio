# Module:   runtime
# date:     17th November 2013
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""runtime"""


from state import State


state = State()


def init(args=[], opts=None):
    global state

    state.args = args
    state.opts = opts

    state.bootstrap()
    state.initialize()


def types(name):
    global state

    return state.root["Types"][name]


def core(name):
    global state

    return state.root["Core"][name]


def find(name):
    global state

    return state.find(name)
