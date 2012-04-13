from lobby import Lobby
from object import Object

from core.number import Number

Object = Object()
Lobby = Lobby(proto=Object)

Lobby["Lobby"] = Lobby
Lobby["Object"] = Object

Lobby["Number"] = Number(0, Object)

Lobby["List"] = Object.clone([])
Lobby["Message"] = Object.clone()
Lobby["String"] = Object.clone("")
Lobby["None"] = Object.clone(None)
Lobby["True"] = Object.clone(True)
Lobby["False"] = Object.clone(False)
