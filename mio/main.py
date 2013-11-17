#!/usr/bin/env python


from traceback import format_exc
from signal import signal, SIGINT, SIG_IGN


import mio
from mio import runtime


USAGE = "mio [-e expr | -i | -S] [file | -]"
VERSION = "mio v" + mio.__version__


class Options(object):

    def setoption(self, name, value):
        setattr(self, name, value)


def parse_bool_arg(name, argv):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del(argv[i])
            return True
    return False


def parse_arg(name, argv):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del(argv[i])
            return argv.pop(i)
    return ""


def parse_args(argv):
    opts = Options()

    opts.setoption("eval", parse_arg("-e", argv))
    opts.setoption("nosys", parse_bool_arg('-S', argv))
    opts.setoption("inspect", parse_bool_arg('-i', argv))
    opts.setoption("help", parse_bool_arg("-h", argv) or parse_bool_arg("--help", argv))
    opts.setoption("version", parse_bool_arg("-v", argv) or parse_bool_arg("--version", argv))

    if opts.help:
        print(USAGE)
        raise SystemExit(0)

    if opts.version:
        print(VERSION)
        raise SystemExit(0)

    del(argv[0])

    return opts, argv


def main(argv):
    try:
        opts, args = parse_args(argv)

        signal(SIGINT, SIG_IGN)

        runtime.init(args, opts)

        if opts.eval:
            runtime.state.eval(opts.eval)
        elif args:
            runtime.state.load(args[0])
            if opts.inspect:
                runtime.state.repl()
        else:
            runtime.state.repl()
    except SystemExit as e:
        return e[0]
    except Exception as e:
        print("ERROR:", e)
        print(format_exc())
        return 1


def entrypoint():
    """SetupTools Entry Point"""

    import sys
    main(sys.argv)


if __name__ == "__main__":
    entrypoint()
