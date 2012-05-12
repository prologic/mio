def pytest_funcarg__mio(request):
    return request.cached_setup(
            setup=lambda: setup_mio(request),
            teardown=lambda mio: teardown_mio(mio),
            scope="module")


def setup_mio(request):
    from mio import runtime
    runtime.init()

    return runtime.state


def teardown_mio(webapp):
    pass
