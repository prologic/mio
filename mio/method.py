from .object import Object

class Method(Object):

    def __init__(self, lobby, context, args, message):
        super(Method, self).__init__()

        self.lobby = lobby
        self.definition_context = context
        self.args = args
        self.message = message

    def __call__(self, receiver, calling_context, *args):
        method_context = self.definition_context.clone()

        method_context["self"] = receiver
        method_context["arguments"] = self.lobby["List"].clone(args)

        for i, arg in enumerate(self.args):
            if i < len(args):
                method_context[arg.name] = args[i](calling_context)
            else:
                method_context[arg.name] = self.lobby["None"](calling_context)


        def __eval_arg(receiver, context, at):
            index = at(context).value
            if index is not None and index < len(args):
                return args[index](calling_context)
            else:
                return self.lobby["None"](calling_context)


        method_context["eval_arg"] = __eval_arg

        return self.message(method_context)
