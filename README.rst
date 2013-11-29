.. _Python Programming Language: http://www.python.org/
.. _How To Create Your Own Freaking Awesome Programming Language: http://createyourproglang.com/
.. _Marc-Andre Cournoye: http://macournoyer.com/
.. _Project Website: http://mio-lang.org/
.. _PyPi Page: http://pypi.python.org/pypi/mio-lang
.. _Read the Docs: http://mio-lang.readthedocs.org/en/latest/
.. _Read the Tutorial: http://mio-lang.readthedocs.org/en/latest/tutorial.html
.. _Downloads Page: https://bitbucket.org/prologic/mio-lang/downloads


mio is a minimalistic IO programming language written in the
`Python Programming Language`_ based on MIo (*a port from Ruby to Python*)
in the book `How To Create Your Own Freaking Awesome Programming Language`_ by
`Marc-Andre Cournoye`_.

This project is being developed for educational purposes only and should serve as
a teaching tool for others wanting to learn how to implement your own programming
language (*albeit in the style of Smalltalk, Io, etc*). Many thanks go to `Marc-Andre Cournoye`_
and his wonderful book which was a great refresher and overview of the overall processing
and techniques involved in programming language design and implementation. Thanks also go to the
guys in the ``#io`` channel on the FreeNode IRC Network specifically **jer** nad **locks**
for their many valuable tips and help.

The overall goal for this project is to create a fully useable and working programming language
implementation of a langauge quite similar to `Io <http://iolanguage.com>`_ with heavy influence
from `Python <http://python.org>`_ (*because Python is awesome!*). This has already largely been
achived in the current version. See the `RoadMap <http://mio-lang.readthedocs.org/en/latest/roadmap.html>`_
for what might be coming up next.

.. warning:: mio is a new programming language in early **Planning** and **Development**.
             DO NOT USE IN PRODUCTION! USE AT YOUR OWN RISK!

- Visit the `Project Website`_
- `Read the Docs`_
- `Read the Tutorial`_
- Download it from the `Downloads Page`_

.. image:: https://pypip.in/v/mio-lang/badge.png
   :target: https://crate.io/packages/mio-lang/
   :alt: Latest PyPI version

.. image:: https://pypip.in/d/mio-lang/badge.png
   :target: https://crate.io/packages/mio-lang/
   :alt: Number of PyPI downloads

.. image:: https://jenkins.shiningpanda-ci.com/prologic/job/mio-lang/badge/icon
   :target: https://jenkins.shiningpanda-ci.com/prologic/job/mio-lang/
   :alt: Build Status

.. image:: https://requires.io/bitbucket/prologic/mio-lang/requirements.png?branch=default
   :target: https://requires.io/bitbucket/prologic/mio-lang/requirements/?branch=default
   :alt: Requirements Status


Examples
--------

Factorial::
    
    Number fact = method(reduce(block(a, x, a * x), range(1, self)))
    
Hello World::
    
    print("Hello World!")
    

Features
--------

- Homoiconic
- Message Passing
- Higher Order Messages
- Higher Order Functions
- Full support for Traits
- Object Orienated Language
- Written in an easy to understand language
- Supports Imperative, Functional, Object Oriented and Behavior Driven Development styles.


Installation
------------

The simplest and recommended way to install mio is with pip.
You may install the latest stable release from PyPI with pip::

    > pip install mio-lang

If you do not have pip, you may use easy_install::

    > easy_install mio-lang

Alternatively, you may download the source package from the
`PyPI Page`_ or the `Downloads page`_ on the `Project Website`_;
extract it and install using::

    > python setup.py install

You can also install the
`latest-development version <https://bitbucket.org/prologic/mio-lang/get/tip.tar.gz#egg=mio-lang-dev>`_ by using ``pip`` or ``easy_install``::
    
    > pip install mio-lang==dev

or::
    
    > easy_install mio-lang==dev


For further information see the `mio documentation <http://mio-lag.readthedocs.org/>`_.
