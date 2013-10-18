class State(object):

    isContinue = False
    isReturn = False
    isNormal = False
    isBreak = False

    def __init__(self, returnValue=None):
        super(State, self).__init__()

        self.returnValue = returnValue

    @property
    def stop(self):
        return not self.isNormal


class NormalState(State):

    isNormal = True


class BreakState(State):

    isBreak = True


class ContinueState(State):

    isContinue = True


class ReturnState(State):

    isReturn = True
