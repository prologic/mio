from sys import exc_info


from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import UserError


class Exception(Object):

    def __repr__(self):
        return "{0:s}({1:s})".format(self.type, self.value or "")

    @method("try")
    def tryEval(self, receiver, context, m, code):
        try:
            return code.eval(context)
        except:
            etype, evalue, _ = exc_info()
            error = etype.__name__
            message = str(evalue)

            return runtime.state.eval("""Error primitive("clone") init("{0:s}", "{1:s}")""".format(error, message))

    @method("raise")
    def raiseError(self, receiver, context, m, error):
        raise UserError(error.eval(context))
