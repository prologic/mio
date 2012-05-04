from state import State
from object import Object

from core.map import Map
from core.file import File
from core.list import List
from core.range import Range
from core.number import Number
from core.string import String
from core.system import System

Object = Object()
Lobby = Object.clone(type="Lobby")

Lobby["Lobby"] = Lobby
Object["Lobby"] = Lobby
Lobby["Object"] = Object

Lobby["Map"] = Map({}, Object)
Lobby["List"] = List([], Object)
Lobby["File"] = File(parent=Object)
Lobby["Number"] = Number(0, Object)
Lobby["String"] = String("", Object)
Lobby["Range"] = Range(parent=Object)

Lobby["None"] = Object.clone(None)
Lobby["True"] = Object.clone(True)
Lobby["False"] = Object.clone(False)

Object["state"] = State(parent=Object)
Lobby["System"] = System(parent=Object)
