# Module:   compile
# Date:     18th June 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""Compile Tasks"""


from __future__ import print_function

from os import getcwd, path


from fabric.tasks import Task
from fabric.contrib.files import exists
from fabric.api import cd, execute, hosts, prefix, run, task

from py.path import local as localpath


from .utils import msg, resolvepath, tobool


# Path to pypy
PYPY = resolvepath("$HOME/work/pypy")


@task(default=True)
@hosts("localhost")
def compile(**options):
    """Compile an executable with RPython

    Options:
        pypy    - Path to pypy repository
        tests   - Whether to run the tests.
        output  - Output filename for mio.
        target  - Target module to compile.
    """

    pypy = resolvepath(options.get("pypy", PYPY))
    tests = tobool(options.get("tests", "yes"))
    output = resolvepath(options.get("output", "./build/mio"))
    target = resolvepath(options.get("target", "./targets/target_mio.py"))

    try:
        with cd(getcwd()):
            with msg("Creating env"):
                run("mkvirtualenv compile")

            with msg("Bootstrapping"):
                with prefix("workon compile"):
                    run("./bootstrap.sh")

            with msg("Building"):
                with prefix("workon compile"):
                    run("fab develop")

            if tests:
                with msg("Running tests"):
                    with prefix("workon compile"):
                        run("fab test")

        build = resolvepath(path.dirname(output))
        if not exists(build):
            run("mkdir {0:s}".format(build))

        options = (
            "--output={0:s}".format(output),
        )

        with cd(pypy):
            with prefix("workon compile"):
                run("python setup.py develop")

        args = (" ".join(options), target)
        with prefix("workon compile"):
            run("rpython {0:s} {1:s}".format(*args))

    finally:
        with msg("Destroying env"):
            run("rmvirtualenv compile")


class Compile(Task):

    name = "test"

    def __init__(self, *args, **kwargs):
        super(Compile, self).__init__(*args, **kwargs)

        self.options = kwargs.get("options", {})

    def run(self):
        return execute(compile, **self.options)


p = localpath()

for target in p.join("targets").listdir("*.py"):
    name = target.purebasename
    name = name.split("_", 1)[1]

    options = {
        "tests": "no",
        "target": str(target),
        "output": str(p.join("build", name))
    }

    task = Compile(name=name, options=options)
    setattr(task, "__doc__", "Compile {0:s} target".format(name))

    globals()[name] = task
