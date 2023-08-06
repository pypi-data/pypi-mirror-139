#!/usr/bin/env python3
"""
Usage
=====

.. code::

    setalgebra ...

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

Example
=======

.. code::

    setalgebra \( file1 + file2 \) x file3 - file4

The following happens in order

1. file1 + file2
2. x file3
3. \- file4
"""

import sys
import textwrap
import setalgebra

USAGE = f"""
    USAGE
        setalgebra ...

    ARGS
        Treat ... as a set-based arithmetic expression of files and operators.
        Files are sets of lines (whitespace stripped).

        Operators from lower to higher precedence
            +   set union
            -   set difference
            x   set intersection
            (   group precedence
            )

        Union and difference has the same precedence.


    EXAMPLE
        setalgebra \( file1 + file2 \) x file3 - file4

        1. file1 + file2
        2. x file3
        3. - file4

    VERSION
        {setalgebra.__version__}
    """


def usage():
    return textwrap.dedent(USAGE).strip()


def main(args=None):
    args = sys.argv[1:]
    if len(args) == 0:
        print(usage())
        sys.exit(0)
    stack = setalgebra.shunting_yard(sys.argv[1:])
    for item in setalgebra.reverse_polish_calculator(stack):
        print(item)


if __name__ == '__main__':
    main()
