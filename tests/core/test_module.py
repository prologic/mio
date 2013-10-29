def test_module(mio, tmpdir, capfd):
    with tmpdir.ensure("foo.mio").open("w") as f:
        f.write("""
            hello = block(
                print("Hello World!")
            )
        """)

    foo = mio.eval("""foo = Module clone("foo", "{0:s}")""".format(str(tmpdir.join("foo.mio"))))
    assert repr(foo) == "Module(name={0:s}, file={1:s})".format(repr("foo"), repr(str(tmpdir.join("foo.mio"))))

    mio.eval("foo hello()")

    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("""del("foo")""")


def test_package(mio, tmpdir, capfd):
    path = tmpdir.ensure("foo", dir=True)

    with path.join("__init__.mio").open("w") as f:
        f.write("""
            hello = block(
                print("Hello World!")
            )

            bar = import(bar)
        """)

    with path.join("bar.mio").open("w") as f:
        f.write("""
            foobar = block(
                print("Foobar!")
            )
        """)

    # Add test package path to search path
    mio.eval("""Importer paths insert(0, "{0:s}")""".format(str(tmpdir)))

    foo = mio.eval("foo = import(foo)")
    assert repr(foo) == "Module(name={0:s}, file={1:s})".format(repr("foo"), repr(str(path.join("__init__.mio"))))

    mio.eval("foo hello()")

    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("foo bar foobar()")

    out, err = capfd.readouterr()
    assert out == "Foobar!\n"

    mio.eval("""del("foo")""")
