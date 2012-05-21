#!/usr/bin/env python

try:
    from coverage import coverage
    HAS_COVERAGE = True
except ImportError:
    HAS_COVERAGE = False

from mio.__main__ import main


if __name__ == "__main__":
    try:
        if HAS_COVERAGE:
            _coverage = coverage(data_suffix=True)
            _coverage.start()
        main()
    finally:
        if HAS_COVERAGE:
            _coverage.stop()
            _coverage.save()
