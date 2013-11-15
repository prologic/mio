# Target:   mio
# Date:     16th November 2013
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""RPython Entry Point: mio"""


from mio.main import main


def target(*args):
    return main, None
