======================
Test Cases Code Blocks
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Code Block Python
=================

.. code-block:: python

    # Python 3: Fibonacci series up to n
    >>> def fib(n):
    >>>     a, b = 0, 1
    >>>     while a < n:
    >>>         print(a, end=' ')
    >>>         a, b = b, a+b
    >>>     print()
    >>> fib(1000)
    0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987


.. code-block:: python
   :emphasize-lines: 3,5

   def some_function():
       interesting = False
       print 'This line is highlighted.'
       print 'This one is not...'
       print '...but this one is.'


.. code-block:: python

    >>> while True print('Hello world')
      File "<stdin>", line 1
        while True print('Hello world')
                       ^
    SyntaxError: invalid syntax


.. code-block:: python

    >>> 10 * (1/0)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ZeroDivisionError: division by zero


.. code-block:: python
    :linenos:

    class Error(Exception):
        """Base class for exceptions in this module."""
        pass

    class InputError(Error):
        """Exception raised for errors in the input.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the error
        """

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message


.. code-block:: python
   :emphasize-lines: 3,5
   :linenos:

   def some_function():
       interesting = False
       print 'This line is highlighted.'
       print 'This one is not...'
       print '...but this one is.'


.. code-block:: python
   :caption: A caption without a inline format.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with **strong** formatted text.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with *emphasis* formatted text.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with ``as code`` formatted text.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with as :subscript:`subscript` formatted text.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with as :superscript:`superscript` formatted text.

   def some_function():
       print 'This one is not...'


.. code-block:: python
   :caption: A caption with as :file:`c:\windows\path` formatted text.

   def some_function():
       print 'This one is not...'
