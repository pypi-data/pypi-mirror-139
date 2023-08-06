==========
setalgebra
==========

https://gitlab.com/jfriis/setalgebra

Arbitrary set calculations using the shunting yard algorithm


Install
=======

To install using pip:

.. code:: shell

   pip install setalgebra


Usage
=====

.. code::

    setalgebra \( file1 + file2 \) x file3 - file4

Treat ... as a set-based arithmetic expression of files and operators.
Files are sets of lines (whitespace stripped).

Operators from lower to higher precedence

.. list-table::

    * - \+
      - set union
    * - \-
      - set difference
    * - x
      - set intersection
    * - (
      - group precedence
    * - )
      -

Union and difference has the same precedence.
