# Module:   conftest
# Date:     12th October 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""pytest config"""


from pytest import fixture


from mio import runtime


runtime.init()


@fixture(scope="session")
def mio(request):
    return runtime.state
