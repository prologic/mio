from lobby import Lobby
from object import Object

from core.list import List
from core.number import Number
from core.string import String

Object = Object()
Lobby = Lobby(parent=Object)

Lobby["Lobby"] = Lobby
Object["Lobby"] = Lobby
Lobby["Object"] = Object

Lobby["List"] = List([], Object)
Lobby["Number"] = Number(0, Object)
Lobby["String"] = String("", Object)

Lobby["None"] = Object.clone(None)
Lobby["True"] = Object.clone(True)
Lobby["False"] = Object.clone(False)
