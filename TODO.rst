TODO
====


- Try changing the calling convention so that method and block calls have to have explicit parenthesis.
- Implement a ``Binding`` object which is set as an internal object for every object that is boubd.
- Somehow work out a way to make applying of ``*args`` and/or ``**kwargs`` as well as everything else.
- Improve the ``Object primitive`` method to allow for nesting primitive calls. e.g: ``1 :__int__(:__format__("{0:b}"))``
- Have another go at implementing operator precedence.
- Add support for Python-style string and byte literals.
- Implement a ``Tuple`` core object.
- Implement a ``Bytes`` core object.
- Implement an ``FFI`` core object.
