from mio import runtime
from mio.parser import parse
from mio.object import Object
from mio.lexer import tokenize
from mio.utils import method, Null


class Parser(Object):

    def __init__(self, value=Null):
        super(Parser, self).__init__(value=value)

        self.create_methods()
        self.parent = runtime.find("Object")

    @method()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
