from lobby import Lobby
from object import Object

from core.list import List
from core.number import Number
from core.boolean import Boolean

Object = Object()
Lobby = Lobby(proto=Object)

Lobby["Lobby"] = Lobby
Object["Lobby"] = Lobby
Lobby["Object"] = Object

Lobby["List"] = List([], Object)
Lobby["Number"] = Number(0, Object)
Lobby["String"] = String("", Object)
Lobby["None"] = Boolean(None, Object)
Lobby["True"] = Boolean(True, Object)
Lobby["False"] = Boolean(False, Object)
