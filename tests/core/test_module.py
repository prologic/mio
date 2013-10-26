def test_module(mio, tmpdir, capfd):
    with tmpdir.ensure("foo.mio").open("w") as f:
        f.write("""
            hello = block(
                print("Hello World!")
            )
        """)

    foo = mio.eval("""foo = Module clone("foo", "{0:s}")""".format(str(tmpdir.join("foo.mio"))))
    assert repr(foo) == "Module(__name__={0:s}, __file__={1:s})".format(repr("foo"), repr(str(tmpdir.join("foo.mio"))))

    mio.eval("foo hello()")

    out, err = capfd.readouterr()
    assert out == "Hello World!\n"

    mio.eval("""del("foo")""")
