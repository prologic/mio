from os import path


import mio
from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import ImportError


class Importer(Object):

    def __init__(self):
        super(Importer, self).__init__()

        self["paths"] = self.build_paths()

        self.create_methods()
        self.parent = runtime.find("Object")

    def build_paths(self):
        paths = ["."]
        paths.append(path.join(path.dirname(mio.__file__), "lib"))
        paths.append(path.expanduser(path.join("~", "lib", "mio")))
        return runtime.find("List").clone(map(runtime.find("String").clone, paths))

    def find_match(self, name, current=None):
        # Temporarily put the package directory in the search path
        paths = [current] if current is not None else []
        paths.extend([path.abspath(path.expanduser(path.expandvars(str(p)))) for p in self["paths"]])

        for p in paths:
            m = path.join(p, "{0:s}.mio".format(name))
            if path.exists(m):
                return m

            m = path.join(p, name, "__init__.mio")
            if path.exists(m):
                return m

    @method("import")
    def _import(self, receiver, context, m, name):
        name = name.name if name.value is None else str(name.eval(context))

        context = context["call"]["target"] if context.type == "Locals" else context

        # Are we importing inside a package?
        if context.type == "Module" and context.file.endswith("__init__.mio"):
            current = path.dirname(context.file)
        else:
            current = None

        match = self.find_match(name, current)

        if match is not None:
            return runtime.state.eval("""Module primitive("clone") init("{0:s}", "{1:s}")""".format(name, match), receiver, context)
        else:
            raise ImportError("No module named {0:s}".format(name))
