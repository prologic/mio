from object import Object

class Method(Object):

    def __init__(self, context, message):
        self.definition_context = context
        self.message = message

        super(Method, self).__init__(Lobby["Method"])

    def __call__(self, receiver, calling_context, *args):
        method_context = self.definition_context.clone()
        method_context["self"] = receiver
        method_context["arguments"] = Lobby["List"].clone(args)

        def __eval_arg(receiver, context, at):
            return (args[at.call(context).value] or Lobby["nil"]).call(
                    calling_context)

        method_context["eval_arg"] = __eval_arg

        return self.message.call(method_context)
