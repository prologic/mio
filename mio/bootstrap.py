import sys

from object import Object
from method import Method

from core.number import Number

Object = Object()
Lobby = Object.clone()

Lobby["Lobby"] = Lobby
Lobby["Object"] = Object
Lobby["List"] = Object.clone([])
Lobby["Method"] = Object.clone()

Lobby["Number"] = Number(0, Object)

Lobby["Message"] = Object.clone()
Lobby["String"] = Object.clone("")
Lobby["None"] = Object.clone(None)
Lobby["True"] = Object.clone(True)
Lobby["False"] = Object.clone(False)


def Object__method(receiver, context, *args):
    arguments, message = args[:-1], args[-1:][0]
    return Method(Lobby, context, arguments, message)


def Lobby__exit(receiver, context, status=0):
    raise SystemExit(status)

Object["method"] = Object__method

Lobby["exit"] = Lobby__exit
