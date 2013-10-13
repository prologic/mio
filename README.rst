.. _Python Programming Language: http://www.python.org/
.. _How To Create Your Own Freaking Awesome Programming Language: http://createyourproglang.com/
.. _Marc-André Cournoye: http://macournoyer.com/
.. _MIT License: http://www.opensource.org/licenses/mit-license.php
.. _funcparserlib: http://pypi.python.org/pypi/funcparserlib
.. _Project Website: https://bitbucket.org/prologic/mio/
.. _PyPi Page: http://pypi.python.org/pypi/mio
.. _Documentation: http://packages.python.org/mio/
.. _Create an Issue: https://bitbucket.org/prologic/mio/issue/new
.. _Downloads Page: https://bitbucket.org/prologic/mio/downloads


mio is a minimalistic IO programming language written in the
`Python Programming Language`_ based on MIo (*a port from Ruby to Python*)
in the book `How To Create Your Own Freaking Awesome Programming Language`_ by
`Marc-André Cournoye`_.


Examples
--------

Factorial:

.. include:: examples/fact.mio
   :code:
   :start-line: 2

Hello World:

.. include:: examples/hello.mio
   :code:
   :start-line: 2


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

    > pip install mio

If you do not have pip, you may use easy_install::

    > easy_install mio

Alternatively, you may download the source package from the
`PyPI Page`_ or the `Downloads page`_ on the `Project Website`_;
extract it and install using::

    > python setup.py install

You can also install the
`latest-development version <https://bitbucket.org/prologic/mio/get/tip.tar.gz#egg=mio-dev>`_ by using ``pip`` or ``easy_install``::
    
    > pip install mio==dev

or::
    
    > easy_install mio==dev


For further information see the `mio documentation <http://mio.readthedocs.org/>`_.
