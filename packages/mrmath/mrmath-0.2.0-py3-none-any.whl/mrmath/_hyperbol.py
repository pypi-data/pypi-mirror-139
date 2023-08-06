# -*- coding: utf-8 -*-

"""Hyperbelfunktionen.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>
"""

import math


def coth(x: float) -> float:
    r"""Kotangens hyperbolicus.

    Parameters
    ----------
    x
        eingabe ist :math:`x = -\infty \dots + \infty  \qquad  x \neq 0`

    Returns
    -------
    float
        :math:`coth(x)`

    Raises
    ------
    ArithmeticError
        wird ausgelöst wenn :math:`x = 0`

    Examples
    --------
    .. testsetup:: hyperbolicus

        from mrmath import coth

    .. doctest:: hyperbolicus

        >>> coth(0)
        Traceback (most recent call last):
            ...
        ArithmeticError

        >>> print( round( coth(1), 5 ) )
        1.31304

    """
    try:
        return 1.0 / math.tanh(x)
    except ZeroDivisionError:
        raise ArithmeticError('Not defined for x=0.') from None
