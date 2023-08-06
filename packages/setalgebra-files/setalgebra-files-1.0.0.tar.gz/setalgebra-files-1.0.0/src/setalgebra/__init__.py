"""
==========
setalgebra
==========

Arbitrary set calculations using the shunting yard algorithm

.. codeauthor:: Jens Friis-Nielsen <jfriis@example.com>

"""

from setalgebra.version import __version__

import sys
import fileinput
import os.path

OPERATORS = ['x','+','-','(',')']

PRECEDENCE = {  'x' : 3,
                '+' : 2,
                '-' : 2  }

ASSOC =      {  'x' : 0, # left
                '-' : 0,
                '+' : 0  }


class UnsupportedArg(Exception):
    """
    Argument is neither an operator or file.
    """


def validate_arg(arg):
    if not (isfile(arg) or arg in OPERATORS or isinstance(arg, set)):
        raise UnsupportedArg(f"'{arg}' neither a file nor an operator")


def isfile(obj):
    return os.path.isfile(str(obj)) or obj == '/dev/stdin'


def parse_set(obj):
    """
    If *obj* is a filename then parse the file and return a set consisting of the lines, each stripped from leading and trailing whitespace.
    Otherwise return *obj*
    """
    if isfile(obj):
        with filehandle(obj) as handle:
            return set(line.strip() for line in handle.readlines())
    else:
        return obj


def filehandle(path):
    if '.gz' == path[-3:]:
        f = gzip.open(path, 'r')
    else:
        f = open(path, 'r')
    return f


def shunting_yard(args):
    """
    Return a Reverse Polish Notation stack from ordered expression in *args*.
    """
    output = []
    stack = []
    for arg in args:
        validate_arg(arg)
        if isfile(arg):
            output.append(arg)
        else:
            if arg == '(':
                stack.append(arg)
            elif arg == ')':
                while len(stack) > 0 and stack[-1] != '(':
                    output.append(stack.pop())
                if len(stack) == 0:
                    raise Exception("Parenthesis mismatch - too many ')'")
                stack.pop() # discard '(' and ')' - can assume there is a '(' so far
            else:
                if len(stack) > 0: # else possible IndexError
                    while len(stack) > 0 and \
                          stack[-1] != '(' and \
                          ((PRECEDENCE[arg] == PRECEDENCE[stack[-1]] and ASSOC[stack[-1]] == 0) or \
                          PRECEDENCE[arg] < PRECEDENCE[stack[-1]]):
                        output.append(stack.pop())
                stack.append(arg)

    while len(stack) > 0:
        o = stack.pop()
        if o == '(':
            raise Exception("Parenthesis mismatch - too many '('")
        output.append(o)
    return output


def intersection(e1, e2):
    """
    Return set intersection of objects *e1* and *e2*.
    Arguments are first parsed by :py:func:`parse_set`.
    """
    e2 = parse_set(e2)
    e1 = parse_set(e1)
    return e1.intersection(e2)
    

def union(e1, e2):
    """
    Return set union of objects *e1* and *e2*.
    Arguments are first parsed by :py:func:`parse_set`.
    """
    e2 = parse_set(e2)
    e1 = parse_set(e1)
    return e1.union(e2)


def difference(e1, e2):
    """
    Return set difference of objects *e1* and *e2*.
    Arguments are first parsed by :py:func:`parse_set`.
    """
    e2 = parse_set(e2)
    e1 = parse_set(e1)
    return e1.difference(e2)


def reverse_polish_calculator(queue):
    """
    Calculate stack results from queue in Reverse Polish Notation using:

    Operators:
    
    - :code:`x`: :py:func:`intersection`
    - :code:`+`: :py:func:`union`
    - :code:`-`: :py:func:`difference`

    Other args are expected to be sets or files to be parsed by :py:func:`parse_set`

    Returns set
    """
    stack = []
    for o in queue:
        if   o == 'x':
            e2 = stack.pop()
            e1 = stack.pop()
            stack.append(intersection(e1, e2))
        elif o == '+':
            e2 = stack.pop()
            e1 = stack.pop()
            stack.append(union(e1, e2))
        elif o == '-':
            e2 = stack.pop()
            e1 = stack.pop()
            stack.append(difference(e1, e2))
        else:
            stack.append(o)
    return stack[0]
