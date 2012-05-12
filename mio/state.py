from object import Object

from core import Number
from core import String
from core import List
from core import Map

from core import File
from core import Range
from core import System


class State(object):

    STATES = ("isBreak", "isReturn",)

    def __init__(self, lobby):
        super(State, self).__init__()

        self.lobby = lobby

        self.reset()

    def reset(self):
        self.returnValue = None
        self.isContinue = False
        self.isReturn = False
        self.isBreak = False

    def stop(self):
        return any([getattr(self, k, False) for k in self.STATES])

    def create_objects(self):
        lobby = self.lobby

        object = Object()

        lobby["Lobby"] = lobby
        lobby["Object"] = object

        object.create_methods()

        lobby["type"] = String("Lobby")
        lobby["parent"] = object

        lobby["Number"] = Number()
        lobby["String"] = String()
        lobby["List"] = List()
        lobby["Map"] = Map()

        lobby["None"] = object.clone(None)
        lobby["True"] = object.clone(True)
        lobby["False"] = object.clone(False)

        lobby["File"] = File()
        lobby["Range"] = Range()
        lobby["System"] = System()

    def find(self, name):
        return self.lobby.attrs[name]
