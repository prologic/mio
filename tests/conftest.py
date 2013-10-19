# Module:   conftest
# Date:     12th October 2013
# Author:   James Mills, j dot mills at griffith dot edu dot au

"""pytest config"""


from pytest import fixture


from mio import runtime


@fixture(scope="module")
def mio(request):
    runtime.init()
    return runtime.state
