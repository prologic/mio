#!/usr/bin/env python

from optparse import OptionParser
from signal import signal, SIGINT, SIG_IGN

import mio
from mio import runtime

USAGE = "%prog [options] ... [-e expr | file | -]"
VERSION = "%prog v" + mio.__version__


def parse_options(argv):
    parser = OptionParser(usage=USAGE, version=VERSION)
    add_option = parser.add_option

    add_option(
        "-e", "",
        action="store", default=None, dest="eval", metavar="expr",
        help="evalulate the given expression and exit"
    )

    add_option(
        "-i", "",
        action="store_true", default=False, dest="interactive",
        help="run interactively after processing the given files"
    )

    add_option(
        "-S", "",
        action="store_true", default=False, dest="nosys",
        help="don't load system libraries"
    )

    opts, args = parser.parse_args(argv)

    return opts, args


def main(argv=None):
    opts, args = parse_options(argv)

    signal(SIGINT, SIG_IGN)

    runtime.init(args, opts)

    if opts.eval:
        runtime.state.eval(opts.eval)
    elif args:
        runtime.state.load(args[0])
        if opts.interactive:
            runtime.state.repl()
    else:
        runtime.state.repl()


# RPython entry pint
def target(*args):
    return main, None
