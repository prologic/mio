from object import Object
from pymethod import pymethod


class Lobby(Object):

    @pymethod()
    def exit(self, status=0):
        raise SystemExit(status)
