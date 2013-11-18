#!/usr/bin/env python

from __future__ import print_function


import mio
from mio import runtime
from mio.utils import format_result


USAGE = "mio [-e expr | -i | -S | -v] [file | -]"
VERSION = "mio v" + mio.__version__


class Options(object):
    """Options Object Container"""


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


def parse_list_arg(name, argv):
    values = []
    arg = parse_arg(name, argv)
    while arg != "":
        values.append(arg)
        arg = parse_arg(name, argv)
    return values


def parse_args(argv):
    opts = Options()

    opts.eval = parse_list_arg("-e", argv)
    opts.nosys = parse_bool_arg('-S', argv)
    opts.inspect = parse_bool_arg('-i', argv)
    opts.verbose = parse_bool_arg("-v", argv)
    opts.help = parse_bool_arg("--help", argv)
    opts.version = parse_bool_arg("--version", argv)

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

        runtime.init(args, opts)

        if opts.eval:
            for eval in opts.eval:
                if opts.verbose:
                    print("mio>", eval)
                result = runtime.state.eval(eval)
                if opts.verbose and result is not None:
                    output = format_result(result)
                    if output is not None:
                        print("===> {0:s}".format(output))
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
        from traceback import format_exc
        print(format_exc())
        return 1


def entrypoint():
    """SetupTools Entry Point"""

    import sys
    main(sys.argv)


if __name__ == "__main__":
    entrypoint()
