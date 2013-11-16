#!/usr/bin/env python

from glob import glob
from imp import new_module
from os import getcwd, path


from setuptools import setup, find_packages


version = new_module("version")

exec(
    compile(open(path.join(path.dirname(globals().get("__file__", path.join(getcwd(), "mio"))), "mio/version.py"), "r").read(), "mio/version.py", "exec"),
    version.__dict__
)


setup(
    name="mio-lang",
    version=version.version,
    description="A Toy Programming Language written in Python",
    long_description="{0:s}\n\n{1:s}".format(
        open("README.rst").read(), open("CHANGES.rst").read()
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
        "funcparserlib==0.3.6",
    ],
    entry_points={
        "console_scripts": [
            "mio=mio.main:entrypoint",
        ]
    },
    test_suite="tests.main.main",
    zip_safe=True
)
