from object import Object
from method import Method

object = Object()
  
def __clone(receiver, context):
    return receiver.clone()

object["clone"] = __clone

def __set_slot(receiver, context, name, value):
    receiver[name.call(context).value] = value.call(context)

object["set_slot"] = __set_slot

def __print(receiver, context):
    print(receiver.value)
    return Lobby["nil"]

object["print"] = __print

Lobby = object.clone()

Lobby["Lobby"]   = Lobby
Lobby["Object"]  = object
Lobby["nil"]     = object.clone(None)
Lobby["true"]    = object.clone(True)
Lobby["false"]   = object.clone(False)
Lobby["Number"]  = object.clone(0)
Lobby["String"]  = object.clone("")
Lobby["List"]    = object.clone([])
Lobby["Message"] = object.clone
Lobby["Method"]  = object.clone

def __method(receiver, context, message):
    return Method(context, message)

Lobby["method"] = __method
