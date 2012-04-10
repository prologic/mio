import sys

from object import Object
from method import Method

object = Object()


def __clone(receiver, context, value=None):
    return receiver.clone(value(context))

object["clone"] = __clone


def __set_slot(receiver, context, name, value):
    receiver[name(context).value] = value(context)
    return receiver[name(context).value]

object["set_slot"] = __set_slot


def __print(receiver, context):
    sys.stdout.write("%s" % receiver.value)
    return receiver

object["print"] = __print

Lobby = object.clone()

Lobby["Lobby"] = Lobby
Lobby["Object"] = object
Lobby["nil"] = object.clone(None)
Lobby["true"] = object.clone(True)
Lobby["false"] = object.clone(False)
Lobby["Number"] = object.clone(0)
Lobby["String"] = object.clone("")
Lobby["List"] = object.clone([])
Lobby["Message"] = object.clone()
Lobby["Method"] = object.clone()


def __method(receiver, context, message):
    return Method(context, message)

Lobby["method"] = __method
