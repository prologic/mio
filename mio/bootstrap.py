import sys

from .object import Object
from .method import Method

Object = Object()
Lobby = Object.clone()

Lobby["Lobby"] = Lobby
Lobby["Object"] = Object
Lobby["List"] = Object.clone([])
Lobby["Method"] = Object.clone()

def Number__add(receiver, context, value):
    return receiver.value + value(context).value

def Number__sub(receiver, context, value):
    return receiver.value - value(context).value

def Number__mul(receiver, context, value):
    return receiver.value * value(context).value

def Number__div(receiver, context, value):
    return receiver.value / value(context).value

Number = Object.clone()

Number["add"] = Number__add
Number["sub"] = Number__sub
Number["mul"] = Number__mul
Number["div"] = Number__div

Lobby["Number"] = Number.clone(0)

Lobby["Message"] = Object.clone()
Lobby["String"] = Object.clone("")
Lobby["None"] = Object.clone(None)
Lobby["True"] = Object.clone(True)
Lobby["False"] = Object.clone(False)


def Object__clone(receiver, context, value=None):
    if value is not None:
        value = value(context)

    return receiver.clone(value)


def Object__set_slot(receiver, context, name, value):
    receiver[name(context).value] = value(context)
    return receiver[name(context).value]


def Object__print(receiver, context):
    sys.stdout.write("%s" % receiver.value)
    return receiver


def Object__method(receiver, context, *args):
    arguments, message = args[:-1], args[-1:][0]
    return Method(Lobby, context, arguments, message)


def Lobby__exit(receiver, context, status=0):
    raise SystemExit(status)

Object["set_slot"] = Object__set_slot
Object["method"] = Object__method
Object["print"] = Object__print
Object["clone"] = Object__clone

Lobby["exit"] = Lobby__exit
