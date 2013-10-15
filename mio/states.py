class StopState(object):

    returnValue = None
    isContinue = False
    isReturn = False
    isBreak = False

    def __init__(self, returnValue=None):
        super(StopState, self).__init__()

        self.returnValue = returnValue


class BreakState(StopState):

    isBreak = True


class ContinueState(StopState):

    isContinue = True


class ReturnState(StopState):

    isReturn = True
