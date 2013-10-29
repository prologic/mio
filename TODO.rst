TODO
====


- Try to chnage the semantics of arguments such that:

  - Arguments are evaluated when blocks/methods are called.
  - A copy of unevaluated arguments are available in the message.

- Somehow work out a way to make applying of ``*args`` and/or ``**kwargs`` as well as everything else.
- Have another go at implementing operator precedence.
- Implement a ``Tuple`` core object.
- Implement a ``Bytes`` core object.

- Do a refresher on how to write an interpreter in RPython and write a really really simple one:

  - http://doc.pypy.org/en/latest/coding-guide.html#restricted-python
  - http://morepypy.blogspot.com.au/2011/04/tutorial-writing-interpreter-with-pypy.html
