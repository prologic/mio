from mio.parser import parse
from mio.utils import method
from mio.object import Object
from mio.lexer import tokenize


class Parser(Object):

    @method()
    def parse(self, receiver, context, m, code):
        code = str(code.eval(context))
        return parse(tokenize(code))
