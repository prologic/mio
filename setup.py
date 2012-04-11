#!/usr/bin/env python

import os
from glob import glob

try:
    from setuptools import setup, find_packages
    HAS_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAS_SETUPTOOLS = False

if not HAS_SETUPTOOLS:
    from distutils.util import convert_path

    def find_packages(where=".", exclude=()):
        """Borrowed directly from setuptools"""

        out = []
        stack = [(convert_path(where), "")]
        while stack:
            where, prefix = stack.pop(0)
            for name in os.listdir(where):
                fn = os.path.join(where, name)
                if ("." not in name and os.path.isdir(fn) and
                        os.path.isfile(os.path.join(fn, "__init__.py"))):
                    out.append(prefix + name)
                    stack.append((fn, prefix + name + "."))

        from fnmatch import fnmatchcase
        for pat in list(exclude) + ["ez_setup"]:
            out = [item for item in out if not fnmatchcase(item, pat)]

        return out

path = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(path, "README.rst")).read()
    RELEASE = open(os.path.join(path, "RELEASE.rst")).read()
except IOError:
    README = RELEASE = ""

setup(
    name="mio",
    description="mio - The Programming Language",
    long_description="%s\n\n%s" % (README, RELEASE),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="http://bitbucket.org/prologic/mio/",
    download_url="http://bitbucket.org/prologic/mio/downloads/",
    classifiers=[],
    license="MIT",
    keywords="toy programming language io mio message",
    platforms="POSIX",
    packages=find_packages("."),
    scripts=glob("scripts/*"),
    entry_points="""
    [console_scripts]
    mio = mio.__main__:main
    """,
    zip_safe=False,
    test_suite="tests.main.runtests",
)

# hghooks: no-pyflakes
