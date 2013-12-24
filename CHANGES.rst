Changes
-------


mio 0.1.8 (*2013-12-24*)
........................

- Implemented ``caller()`` [**functools**]
- Fixed parser support for ``[1] + [2]`` --> ``[](1} +([](2))``
- Fixed ``List extend()`` to take another list, not ``*args``.
- Implemented ``+`` List operator.
- Implemented ``min`` and ``max`` and added to the mio std. lib.


mio 0.1.7 (*2013-12-09*)
........................

- Fixed ``Object evalArg()`` so it can take zero arguments and return ``None``. e.g: ``() a``
- Implemented ``identity()`` and ``constantly()`` in ``functools`` std. lib and added unit tests.
- Fixed typos in ``operators`` module.
- Moved all trait related user methods to ``TAdaptable`` core trait.
- Added ``adapt()`` method to ``TAdaptable``.

.. note:: This is more or less an alias of ``use()`` except the object
          being adapted is cloned and the original left in tact. The
          adaptation is therefore temporary.

- Added support for contextually aware tab completion.
- Test Coverage back up to 100%


mio 0.1.6 (*2013-12-04*)
........................

- Added support for packaging Python `wheels <http://pythonwheels.com/>`_.
- Define a default ``init()`` method on ``Object`` and just make ``TCloneable init()`` just call ``init()``.
- Added ``String strip()`` method.
- Make ``String`` use ``TIterable``.
- Implemented ``input()`` builtin.
- Implemented a special object ``Trait`` which all traits are cloend from.

  - This means traits now cannot contain state and a ``TypeError`` is raised.
  - Objects can only use or add traits that are inherited from the ``Trait`` object.

A simple trait thus looks like::
    
    TFoo = Trait clone() do (
        foo = method(
            print("Foo!")
        )
    )
    
- Implemented ``Trait requires()`` so that traits can declare the names of methods and attribute they depend on.

e.g::
    
    TGreetable = Trait clone() do (
        requires("name")
    
        hello = method(
            print("Hello ", self name)
        )
    )
    
    World = Object clone() do (
        name = "World!"
        uses(TGreetable)
    )
    
    World hello()
    
- Added conflict resolution for traits.
- Remvoed ``uses`` in favor of single ``use(trait, resolution)`` where **resolution** is a dict of key->value pairs that rename
  conflicting methods of the trait being used.
- Make ``Object hasTrait()`` lookup the parent chain.
- Abuse the ``is`` method of ``TComparble`` to be used as short-cut for: ``foo hasTrait(TFoo)``.


mio 0.1.5 (*2013-11-28*)
........................

- Don't look into ``builtins`` module for the tab-completer function of the REPL if there are no builtins. i.e: ``mio -S``
- Added a nice big shiny red warning about mio's status.


mio 0.1.4 (*2013-11-27*)
........................

- Added "Functions" to the tutorial.
- Added "Objects" to the tutorial.
- Added "Traits" to the tutorial.
- Added the start of a small ``functools`` library to the mio std. lib.
- Added ``test_builtins`` to mio. std library as a tests package.
- Added operators module to mio std. lib.
- Rought cut of generators implemented in CPython and mio.
- Implemented ``KeyError`` exception type and used this to guard non-existent key lookups on dicts.
- Somewhat improved the error handling and tracebacks.
- Improved the way generators work.
- Added ``yield`` to the mio std lib builtins.
- Added ``TypeError`` guard around opening non-files with the ``Path`` object.
- Rewrote the tutorial to utilize ``sphinxcontrib-autorun`` extension with custom ``miointerpreter.py`` module.
- Improved REPL continuation output of unclosed parens.
- Removed docs dependencies of unused sphinx extensions.
- Added ``mio.state.State.runsource()`` which simplifies ``mio.state.State.repl()`` a bit and allows our custom ``sphinxcontrib-autorun`` ext to work.
- Added API Docs.


mio 0.1.3 (*2013-11-19*)
........................

- Fixed tutorial by writing a bash script that generates it (*Read the Docs forbids program-output extension*).


mio 0.1.2 (*2013-11-19*)
........................

- Moved ``File`` from types to core.
- Allow multiple ``-e expr`` options to be given on the CLI.
- Implemented ``len`` builtin.
- Implemented ``List remove()`` method.
- Implemented ``String split()`` method. 
- Implemented ``String __getitem__()`` and ``String __len__()`` methods.
- Implemented ``Bytes __getitem__()`` and ``Bytes __len__()`` methods.
- Added ``[]`` syntactic sugar to ``Bytes`` and ``String`` objects.
- Wrote a basic `mio tutorial <http://mio-lang.readthedocs.org/en/latest/tutorial.html>`_
- Updated the factorial example to be a little clearer.
- Improved Test Coverage of new features and objects.


mio 0.1.1  (*2013-11-18*)
.........................

- The beginnings of a testing framework.
- Implemented unit tests for mio builtins: ``abs``, ``all`` and ``any``.
- Added paren detection to the REPL so you start write long functions over multiple lines. (*Borrowed from: https://bitbucket.org/pypy/lang-scheme/src/b1d5a1b8744f3c7c844775cb420c1a5d4c584592/scheme/interactive.py?at=default*).
- Added basic tab completion support to the REPL.

.. note:: This is not context aware and build up a list of known objects from ``Root``, ``Types``, ``Core`` and ``builtins``.

- Many RPython compilation issues fixed.
- Implemented ``Path`` object.


mio 0.1 (*2013-11-14*)
......................

- Updated factorial examples
- Added support for and a ``fab compile`` task for compiling mio with RPython

.. warning:: This does not work yet!

- Changed the way results are printed on the REPL by implementing a ``format_value(...)`` utility function.
- Added ``assert`` as a special name (*operator*).
- Added optional message argument to ``assert``.
- Improved repr of ``Core`` and ``Types`` objects.
- Fixed a bug in the parser so that we can use ``[]`` and ``{}`` as methods.

::
    
    xs = [1, 2, 3, 4]
    xs[0]
    
- Implemented dict literals.

::
    
    {"a": 1, "b": 2}
    
.. note:: This only works with keys as strings for the moment.

- Added a ``hash`` builtin.
- Improved ``{}`` dict literal so that any hashable keys can be used.

.. note:: Like Python this means any object whoose ``__hash__()`` method
          returns a non-``None`` value.

- Fixed ``any`` and ``all`` builtins.
- IMplemented ``in`` method of ``TComparable``

::
    
    1 in(1, 0)
    
- Changed the semantics of closures.

  - ``this`` is a new attribute of ``Locals`` that always references the
    current block scope.
  - ``self`` is a reference to the current object in scope (*if there is one*).

.. warning:: This behavior may change as I'm not 100% happy with this.

.. note:: This is sort of a work-around to allow blocks to access the
          currently scoped object ``self`` inside the scope of a method
          or nested blocks within a method.


mio 0.0.9 (*2013-11-10*)
........................

- Fixed ``[]`` syntax for creating lists.
- Fixed ``TIterable foreac`` to work more like a for loop.
- Introduced properties for internal Python Functions exposed to mio.
- Adopted calling with ``(...)``'s for all methods.
- Also format functions in ``format_object(...)``.
- Added ``__call__`` to ``Error`` objects. This allows:

::
    
    raise TypeError("foo")

- Added iterator support for ``Range`` object.
- Renamed ``str`` and ``repr`` methods of ``Object`` to ``__str__`` and ``__str__`` respectively and implemtned ``str`` and ``repr`` builtins.
- Optimized the tokenizer
- Added ``ifError``, ``ifNonError`` and ``catch`` to the ``Object`` object to deal with non-errors.
- Improved and fixed a lot of the builtins.
- Improved the way ``*args`` is handled (*still needs more work*).
- Implemented ``assert`` builtin.


mio 0.0.8 (*2013-11-07*)
........................

- Removed operator precedence parsing.

  - Operator precedence is **HARD**
  - Operator precedence rules hare **HARD** to remember
  - Operator precedence is not the main goal of mio right now.

- Tidied up the builtins module.
- ``from foo import *`` works again (*operator precedence parsing broke it*).


mio 0.0.7 (*2013-11-06*)
........................

- Added rudamentary stack trace support to errors. A somewhat "okay" stack trace is displayed on error(s).
- Added ``String format`` method for performing string iterpolation. Only supports ``{0}``, ``{1}``, etc.
- Implemented ``ListIterator`` iterable object with ``iter`` added to mio std. lib. This works similiarly to Python's iterators:

::
    
    mio> xs = [1, 2, 3, 4]
    ===> list(1, 2, 3, 4)
    mio> it = iter(xs)
    ===> ListIterator(list(1, 2, 3, 4))
    mio> it next()
    ===> 1
    mio> it next()
    ===> 2
    mio> it next()
    ===> 3
    mio> it next()
    ===> 4
    
A further iteration would result in:

::
    
    mio> it next()

      StopIteration: 
      --------------
      next
    ifFalse(
     raise(StopIteration) 
    ) 

    raise(StopIteration) 
    
- Re-implemented ``return`` function as part of the mio std. lib.
- Don't allow ``return`` to be called outside of a ``Block`` (*block/method*) as this is illegal.
- Implemented ``while`` builtin as part of the mio std. lib.
  (*no break or continue support yet*)
- Implemented ``loop`` builtin as part of the mio std. lib.
  (*no break or continue support yet*)
- Implemented basic support for reshuffling messages before chaining to support ``x is not None`` --> ``not(x is None)``.
- Finally implemented operator precedence support (*which seems to cover most edge cases*).

.. note:: Need to write lots of unit tests for this!

- Fixed all found edge cases with the new operator precedence lexer/parser.
- Improved ``Error`` object and added ``Error catch`` method for catching errors.
- Implemented ``reduce`` builtin.
- Implemented TComparable trait
- Implemented TCloneable trait
- Iterpret ``call message args`` to mean "pass all args to the callable"
- Imroved Dict and List objects.
- Implemented ``__call__`` calling semantics whereby an object can implement this as a method and ``Foo()`` will invoke ``Foo __call__`` if it exists.
- IMplemented the ``__get__`` part of the Data Descriptor protocol.


mio 0.0.6 (*2013-11-02*)
........................

- Allow an optional object to be passed to the ``Object id`` method.
- Implemented ``hex`` builtin.
- Implemented ``Bytes`` and ``Tuple`` objects.
- Implemented ``State`` core object and sample ``loop`` builtin (*in testing*).
- Refactored all of the context state management code (*stopStatus*) and exposed it to the end user.

  - This means we can now write flow based constructs such as loops directly in mio.

- Fixed a minor bug in the parser where ``not(0) ifTrue(print("foo"))`` would parse as ``not(0, ifTrue(print("foo")))``
- Fixed a minor bug in the parser where ``isError`` would parse as ``is(Error)``. Parse identifiers before operators.
- Implemented basic excpetion handling and error object(s) (*no stack traces yet*).
- Moved ``exit`` to builtins.
- Moved the setting of ``.binding`` attribute to ``Object`` ``set/del`` methods.
- Added support for ``..`` operator and added this to ``Number``. This allows you to write:

::
    
    x = 1 .. 5  # a Range from 1 to 5
    
- Added ``+`` and ``-`` operators to the ``Range`` object so you can do things like:

::
    
    x = (1 .. 5) + 2  # a Range from 1 to 5 in increment of 2
    
- Changed default REPL prompt to: 

::
    
    $ mio
    mio 0.0.6.dev
    mio>
    
- Implemented ``sum`` builtin.
- Added ``try`` and ``raise`` builtins. (*``raise`` is not implemented yet...*).
- Added support for User level Error(s) and implemented ``Exception raise``
- Replaced ``Continuation call`` with activatable object semantics. This means:

::
    
    c = Continuation current()
    print("foo")
    c()
    
- ``Object evalArg`` should evaluate the argument with context as the receiver.
- Added ``List __getitem__`` and ``List __len__`` methods.
- Added ``TIterable`` trait to the mio bootstrap library and added this to ``List``.
- Removed ``foreach``, ``whilte``, ``continue``, ``break`` and ``return`` ``Object`` methods. These will be re-implemented as traits and builtins.
- Changed the way the parser parses and treats operators. They are no longer parsed in a deep right tree.

Example::
    
    1 + 2 * 3

OLD::
    
    1 +(2 *(3))
    
NEW::
    
    1 +(2) *(3)
    
- This will probably make reshuffling and therefore implementing operator precedence a lot easier.
- This also makes the following expressions possible (*used in the builtins module*):

::
    
    from foo import *
    
- Added ``TypeError``, ``KeyError`` and ``AttributeError`` to the mio std. lib.
- Made it possible to import members from a module with: ``from foo import bar``


mio 0.0.5 (*2013-10-29*)
........................

- Split up core into core and types.
- Re-implemented ``True``, ``False`` and ``None`` in mio.
- Implemented ``bin`` builtin.
- Implemented ``bool`` builtin.
- Implemented ``callable`` builtin.
- Implemented ``cha`` builtin.
- IMplemented ``from`` and ``import`` builtins.
- Make the ``Object pimitive`` ``:foo`` method return the internal Python data type.
- Fixed the ``abs`` builtin to return an newly cloned Number.
- Implemented support for packages ala Python.
- Restructured the mio std. lib
- mio nwo bootstraps itself via an import of the "bootstrap" package.
- Reimplemented ``Object clone`` in the mio std. lib.


mio 0.0.4 (*2013-10-27*)
........................

- Moved the implementation of ``super`` to the mio std. lib
- Only set ``_`` as the last result in the Root object (*the Lobby*)
- Added support for ``()``, ``[]`` and ``{}`` special messages that can be used to define syntactic suguar for lists, dicts, etc.
- Implemented ``Dict`` object type and ``{a=1, b=2}`` syntactic sugar to the builtint (*mio std. lib*) ``dict()`` method.
- Refactored the ``File`` object implementation and made it's repr more consistent with other objects in mio.
- Fixed keyword argument support.
- Fixed a few minor bugs in the ``Message`` object and improved test coverage.
- Added ``?`` as a valid operator and an implementation of ``Object ?message`` in the mio std. lib.
- Fixed a bug with ``Range``'s internal iterator causing ``Range asList`` not to work.
- Fixed a bug with ``Object foreach`` and ``continue``.
- **Achived 100% test coverage!**
- Implemented ``*args`` and ``**kwargs`` support for methods and blocks.
- Removed ``Object`` methods ``print``, ``println``, ``write`` and ``writeln`` in favor of the new builtin ``print`` function in the mio std. lib
- Added an implemenation of ``map`` to the mio std. lib
- Fixed a bug with the parser where an argument's previous attribute was not getting set correctly.
- Reimplemented ``not`` in the mio std. lib and added ``-=``, ``*=`` and ``/=`` operators.
- Added a ``Object :foo`` (*primitive*) method using the ``:`` operator. This allows us to dig into the host object's internal methods.
- Added an implementation of ``abs`` builtin using the primitive method.
- Changed the ``import`` function to return the imported module (*instead of ``None``*) so you can bind imported modules to explicitly bound names.
- Added ``from`` an alias to ``import`` and ``Module import`` so you can do:

::
    
    bar = from(foo) import(bar)
    
- Fixed some minor bugs in ``Object foreach`` and ``Object while`` where a ReturnState was not passed up to the callee.
- Added implementations of ``all`` and ``any`` to the mio std. lib.
- Added this.mio (The Zen of mio ala Zen of Python)
- Added List insert method and internal __len__.
- Moved the implementations of the ``Importer`` and ``Module`` objects to the host language (*Python*).
- Added support for modifying the ``Importer`` search path.
- Restructured the mio std. library and moved all bootstrap modules into ./lib/bootstrap
- Added (almost) Python-style string literal support. Triple Quote, Double, Quote, Single Quote, Short and Long Strings
- Added support for exponents with number literals.
- Added internal ``tomio`` and ``frommio`` type converion function.
- Added an ``FFI`` implementation that hooks directly into the host language (*Python*).
- Implemented the ``antigravity`` module in mio.
- Added support for exposing builtin functions as well in the FFI.
- Simplified the two examples used in the docs and readme and write a simple bash script to profile the factorial example.
- Changed the calling semantics so that calls to methods/blocks are explicitly made with ``()``.
- Added a new internal attribute to ``Object`` called ``binding`` used to show the binding of a bound object in repr(s).


mio 0.0.3 (*2013-10-20*)
........................

- Improved test coverage
- Improved the ``Range`` object
- Fixed the scoping of ``block`` (s).
- Fixed the ``write`` and ``writeln`` methods of ``Object`` to not join arguments by a single space.
- Don't display ``None`` results in the REPL.
- Improved the ``__repr__`` of the ``File`` object.
- Added ``open`` and ``with`` builtins to the mio standard library.
- Implemented a basic import system in the mio standard library.
- Implemented ``Dict items`` method.


mio 0.0.2 (*2013-10-19*)
........................

- Include lib as package data
- Allow mio modules to be loaded from anywhere so mio can be more usefully run from anywhere
- Added bool type converion
- Improved the documentation and added docs for the grammar
- Changed Lobby object to be called Root
- Added an -S option (don't load system libraries).
- Added unit test around testing for last value with return
- Refactored Message.eval to be non-recursive
- Set _ in the context as the last valeu
- Implemented Blocks and Methods
- Fixed return/state issue by implementing Object evalArg and Object evalArgAndReturnSelf in Python (not sure why this doesn't work in mio itself)
- Implemented Object evalArgAndReturnNone


mio 0.0.1 (*2013-10-19*)
........................

- Initial Release
