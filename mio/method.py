from utils import method
from object import Object


class Method(Object):

    def __init__(self, context, args, message, parent=None):
        super(Method, self).__init__(parent=parent)

        self.definition_context = context
        self.args = args
        self.message = message

    def __repr__(self):
        return "method(...)"

    def __call__(self, receiver, calling_context, *args):
        method_context = self.definition_context.clone()

        method_context["self"] = receiver
        method_context["caller"] = calling_context
        method_context["args"] = self.lobby("List").clone(args)

        for i, arg in enumerate(self.args):
            if i < len(args):
                method_context[arg.name] = args[i](calling_context)
            else:
                method_context[arg.name] = self.lobby("None")(
                        calling_context)

        self["state"].reset()

        return self.message(method_context)
