from utils import method
from object import Object
from bootstrap import Lobby


class Method(Object):

    def __init__(self, context, args, message):
        super(Method, self).__init__()

        self.definition_context = context
        self.args = args
        self.message = message

    def __repr__(self):
        return "method(...)"

    def __call__(self, receiver, calling_context, *args):
        method_context = self.definition_context.clone()

        method_context["self"] = receiver
        method_context["caller"] = calling_context
        method_context["arguments"] = Lobby["List"].clone(args)

        for i, arg in enumerate(self.args):
            if i < len(args):
                method_context[arg.name] = args[i](calling_context)
            else:
                method_context[arg.name] = Lobby["None"](
                        calling_context)

        return self.message(method_context)

    @method()
    def eval_arg(self, receiver, context, at):
        args = context["args"]
        index = at(context).value
        caller = context["caller"]
        if index is not None and index < len(args):
            return args[index](caller)
        else:
            return Lobby["None"](caller)
