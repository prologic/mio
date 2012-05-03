from utils import Null
from object import Object


class State(Object):

    STOP_STATES = ["isBreak", "isReturn", "stopLooping"]

    def __init__(self, value=Null, parent=None):
        super(State, self).__init__(value=value, parent=parent)

        self.reset()

    def reset(self):
        self["stopLooping"] = self["False"]
        self["isContinue"] = self["False"]
        self["isReturn"] = self["False"]
        self["isBreak"] = self["False"]
        self["return"] = self["None"]

    def stop(self):
        return any([self[k].value for k in self.STOP_STATES])
