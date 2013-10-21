def test_basic_trait(mio, capsys):
    mio.eval("""
        TGreeting = Object clone do (
            hello = method(
                writeln("Hello ", self getGreeting)
            )
        )

        World = Object clone do (
            uses(TGreeting)

            greeting = "World!"

            getGreeting = method(
               return (self greeting)
            )

            setGreeting = method(aGreeting,
                self greeting = aGreeting
            )
        )
    """)

    mio.eval("World hello")
    out, err = capsys.readouterr()
    assert out == "Hello World!\n"

    mio.eval("World setGreeting(\"John\")")
    mio.eval("World hello")
    out, err = capsys.readouterr()
    assert out == "Hello John\n"
