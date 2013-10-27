#!/usr/bin/env python


import hotshot
import hotshot.stats


from mio import runtime

runtime.init()
runtime.state.load("fact.mio")

profiler = hotshot.Profile("fact.profile")
profiler.start()

for i in xrange(100):
    runtime.state.eval("10 fact()")

profiler.stop()
profiler.close()

stats = hotshot.stats.load("fact.profile")
stats.strip_dirs()
stats.sort_stats("time", "calls")
stats.print_stats(20)
