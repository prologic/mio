import sys

from .object import Object

object = Object()


def __clone(receiver, context, value=None):
    if value is not None:
        value = value(context)

    return receiver.clone(value)

object["clone"] = __clone


def __set_slot(receiver, context, name, value):
    receiver[name(context).value] = value(context)
    return receiver[name(context).value]

object["set_slot"] = __set_slot


def __print(receiver, context):
    sys.stdout.write("%s" % receiver.value)
    return receiver

object["print"] = __print

Lobby = object.clone()

Lobby["Lobby"] = Lobby
Lobby["Object"] = object
Lobby["None"] = object.clone(None)
Lobby["True"] = object.clone(True)
Lobby["False"] = object.clone(False)
Lobby["Number"] = object.clone(0)
Lobby["String"] = object.clone("")
Lobby["List"] = object.clone([])
Lobby["Message"] = object.clone()
Lobby["Method"] = object.clone()


class Method(Object):

    def __init__(self, context, args, message):
        self.definition_context = context
        self.args = args
        self.message = message

        super(Method, self).__init__(Lobby["Method"])

    def __call__(self, receiver, calling_context, *args):
        method_context = self.definition_context.clone()

        method_context["self"] = receiver
        method_context["arguments"] = Lobby["List"].clone(args)

        for i, arg in enumerate(self.args):
            if i < len(args):
                method_context[arg.name] = args[i](calling_context)
            else:
                method_context[arg.name] = Lobby["None"](calling_context)


        def __eval_arg(receiver, context, at):
            index = at(context).value
            if index is not None and index < len(args):
                return args[index](calling_context)
            else:
                return Lobby["None"](calling_context)


        method_context["eval_arg"] = __eval_arg

        return self.message(method_context)


def __method(receiver, context, *args):
    arguments, message = args[:-1], args[-1:][0]
    return Method(context, arguments, message)

Lobby["method"] = __method
