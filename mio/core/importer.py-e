from os import path


from funcy import compose, first, imap, izip, repeat, select
from pkg_resources import resource_filename, resource_listdir


import mio
from mio import runtime
from mio.object import Object
from mio.utils import method, Null
from mio.errors import ImportError


class Importer(Object):

    def __init__(self, value=Null):
        super(Importer, self).__init__(value=value)

        self["paths"] = self.build_paths()

        self.create_methods()
        self.parent = runtime.find("Object")

    def build_paths(self):
        paths = ["."]
        paths.append(path.dirname(resource_filename(mio.__package__, path.join("lib", first(resource_listdir(mio.__package__, "lib"))))))
        paths.append(path.expanduser("~/lib/mio"))
        return runtime.find("List").clone(map(runtime.find("String").clone, paths))

    @method("import")
    def _import(self, receiver, context, m, name):
        name = name.eval(context)
        file = "{0:s}.mio".format(name)

        paths = (
            compose(path.abspath, path.expanduser, path.expandvars)(path.join(*p))
            for p in izip(imap(str, self["paths"]), repeat(file, len(self["paths"])))
        )
        filename = first(select(path.exists, paths))

        if filename is not None:
            return runtime.state.eval("""Module clone("{0:s}", "{1:s}")""".format(name, filename), receiver, context)
        else:
            raise ImportError("No module named {0:s}".format(name))
