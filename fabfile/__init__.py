# Package:  fabfile
# Date:     18th June 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""Fabric fabfile"""


from fabric.api import execute, hide, lcd, local, settings, task

from .utils import pip, requires, tobool


@task()
@requires("pip")
def build(**options):
    """Build and install required dependencies

    Options can be provided to customize the build. The following options are supported:

    - dev -> Whether to install in development mode (Default: Fase)
    """

    dev = tobool(options.get("dev", False))

    pip(requirements="requirements{0:s}.txt".format("-dev" if dev else ""))

    with settings(hide("stdout", "stderr"), warn_only=True):
        local("python setup.py {0:s}".format("develop" if dev else "install"))


@task()
def clean():
    """Clean up build files and directories"""

    files = ["build", ".converage", "coverage", "dist", "docs/build"]

    local("rm -rf {0:s}".format(" ".join(files)))

    local("find . -type f -name '*~' -delete")
    local("find . -type f -name '*.pyo' -delete")
    local("find . -type f -name '*.pyc' -delete")
    local("find . -type d -name '__pycache__' -delete")
    local("find . -type d -name '*egg-info' -exec rm -rf {} +")


@task()
def develop():
    """Build and Install in Development Mode"""

    return execute(build, dev=True)


@task()
@requires("make", "sphinx-build")
def docs(**options):
    """Generate the Sphinx documentation

    The following options are recognized:

    - ``clean`` - Perform a clean of the docs build
    - ``view``  - Open a web browser to display the built documentation
    """

    clean = tobool(options.get("clean", False))
    view = tobool(options.get("view", False))

    with lcd("docs"):
        pip(requirements="requirements.txt")
        local("make clean html") if clean else local("make html")

        if view:
            local("open build/html/index.html")


@task()
@requires("py.test")
def test(*args):
    """Run all unit tests and doctests."""

    local("python setup.py test")
