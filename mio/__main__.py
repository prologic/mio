#!/usr/bin/env python

from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

import mio
from mio.interpreter import Interpreter

USAGE = "%prog [options] ... [-c cmd | file | -] [arg] ..."
VERSION = "%prog v" + mio.__version__

modules = (
        "lib/operators.mio",
        "lib/boolean.mio",
        "lib/if.mio",
)


def parse_options():
    parser = OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-c", "",
            action="store", default=None, dest="cmd", metavar="cmd",
            help="program passed in as string (terminates option list)")

    parser.add_option("-i", "",
            action="store_true", default=False, dest="inspect",
            help="inspect interactively after running script")

    parser.add_option("-d", "",
            action="store_true", default=False, dest="debug",
            help="debug output from parser; also MIODEBUG=x")

    opts, args = parser.parse_args()

    return opts, args


def main():
    opts, args = parse_options()

    signal(SIGINT, SIG_IGN)

    interpreter = Interpreter(opts, modules)

    if opts.cmd:
        print(repr(interpreter.eval(opts.cmd)))
    elif args:
        interpreter.load(args[0])
        if opts.inspect:
            interpreter.repl()
    else:
        interpreter.repl()

if __name__ == "__main__":
    main()
