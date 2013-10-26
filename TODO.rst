TODO
====


- Implement a ``Binding`` object which is set as an internal object for every object that is boubd.
- Somehow work out a way to make applying of ``*args`` and/or ``**kwargs`` as well as everything else.
- Improve the ``Object primitive`` method to allow for nesting primitive calls. e.g: ``1 :__int__(:__format__("{0:b}"))``
- Have another go at implementing operator precedence.
- Implement a ``Tuple`` core object.
- Implement a ``Bytes`` core object.

- Do a refresher on how to write an interpreter in RPython and write a really really simple one:

  - http://doc.pypy.org/en/latest/coding-guide.html#restricted-python
  - http://morepypy.blogspot.com.au/2011/04/tutorial-writing-interpreter-with-pypy.html
