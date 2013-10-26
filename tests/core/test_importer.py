from pytest import raises


from mio.errors import ImportError


def test_importer(mio, tmpdir, capfd):
    with tmpdir.ensure("foo.mio").open("w") as f:
        f.write("""
            hello = block(
                print("Hello World!")
            )
        """)

    mio.eval("""Importer paths insert(0, "{0:s}")""".format(str(tmpdir)))
    assert str(tmpdir) in list(mio.eval("Importer paths"))

    mio.eval("foo = import(foo)")
    mio.eval("foo hello()")

    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("""del("foo")""")


def test_import_failure(mio):
    with raises(ImportError):
        mio.eval("import(blah)", reraise=True)
