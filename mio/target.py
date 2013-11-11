# Module:   target
# Date:     11th November 2013
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""RPython Entry Point"""


def main(argv):
    print("Hello World!")
    return 0


def target(*args):
    return main, None
