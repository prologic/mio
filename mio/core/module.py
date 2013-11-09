from os import path


from mio import runtime
from mio.parser import parse
from mio.object import Object
from mio.lexer import tokenize
from mio.utils import method, Null


class Module(Object):

    def __init__(self, value=Null):
        super(Module, self).__init__(value=value)

        self.file = None
        self.name = None

        self.create_methods()
        self.parent = runtime.find("Object")

    def __repr__(self):
        return "Module(name={0:s}, file={1:s})".format(repr(self.name), repr(self.file))

    @method()
    def init(self, receiver, context, m, name, file):
        receiver.name = name = str(name)
        receiver.file = file = str(file)

        # Are we loading a package module?
        if path.isdir(file):
            file = path.join(file, "__init__.mio")

        runtime.state.load(file, receiver, receiver)

        return receiver

    @method("import")
    def _import(self, receiver, context, m, name):
        name = name.name if name.value is None else str(name.eval(context))

        # In case we're importing from inside a module.
        if context.type == "Module" and receiver is context:
            m = parse(tokenize("""Importer import("{0:s}")""".format(name)))
            return m.eval(receiver, context, m)

        if name == "*":
            context.attrs.update(receiver.attrs)
        else:
            context[name] = receiver[name]

        return runtime.find("None")
