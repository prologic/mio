#!/usr/bin/env python

from glob import glob

from setuptools import setup, find_packages


import mio as pkg


setup(
    name="mio-lang",
    version=pkg.__version__,
    description=pkg.__doc__.split("\n")[0],
    long_description="{0:s}\n\n{1:s}".format(
        open("README.rst").read(), open("RELEASE.rst").read()
    ),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="http://bitbucket.org/prologic/mio-lang/",
    download_url="http://bitbucket.org/prologic/mio-lang/downloads/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Interpreters",
    ],
    license="MIT",
    keywords="toy programming language io mio message",
    platforms="POSIX",
    packages=find_packages("."),
    package_data={
        "mio": [
            "lib/*.mio",
        ]
    },
    include_package_data=True,
    scripts=glob("bin/*"),
    install_requires=[
        "funcparserlib",
    ],
    entry_points={
        "console_scripts": [
            "mio=mio.main:main",
        ]
    },
    test_suite="tests.main.main",
    zip_safe=True
)
