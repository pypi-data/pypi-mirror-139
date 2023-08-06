"""
Test for the module mod:`mrmath`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>
"""

from math import isclose

import pytest
from mrmath import coth, ddd, dms, iseven, isodd, modulo


def test_ddd() -> None:
    """Test function `ddd`."""
    assert isclose(ddd(15, 30, 0.0), 15.5)
    assert isclose(ddd(-8, 9, 10.0), -8.15277777777777777)
    assert isclose(ddd(0, 1, 0), 0.0166666666666)
    assert isclose(ddd(0, -5, 0), -0.0833333333333333333)


def test_dms() -> None:
    """Test function `dms`."""
    assert dms(15.5000000000000000000) == (15, 30, 0)
    assert dms(-8.1527777777777777778) == (-8, 9, 10.000000000002842)
    assert dms(0.0166666666666666667) == (0, 1, 0)
    assert dms(-0.0833333333333333333) == (0, -5, 0)
    assert dms(-0.00277777777777777777777) == (0, 0, -10.000000000000002)


def test_coth_01() -> None:
    """Test: coth."""
    assert isclose(coth(1), 1.31303528550)


def test_coth_02() -> None:
    """Test: coth."""
    with pytest.raises(ArithmeticError):
        coth(0)


def test_iseven_01() -> None:
    """Test: iseven."""
    assert iseven(2)
    assert iseven(-2)
    assert iseven(0)


def test_iseven_02() -> None:
    """Test: iseven."""
    assert not iseven(1)
    assert not iseven(-1)
    assert not iseven(9)


def test_isodd_01() -> None:
    """Test: isodd."""
    assert isodd(1)
    assert isodd(-1)
    assert isodd(9)


def test_isodd_02() -> None:
    """Test: isodd."""
    assert not isodd(2)
    assert not isodd(-2)
    assert not isodd(0)


def test_modulo() -> None:
    """Test: modulo."""
    assert isclose(modulo(370, 360), 10.0)
    assert isclose(modulo(-370, 360), 350.0)
    assert isclose(modulo(-30, 360), 330.0)
    assert isclose(modulo(-0, 360), 0.0)
    assert isclose(modulo(360, 360), 0.0)
    assert isclose(modulo(370, -360), -10.0)
    assert isclose(modulo(-370, -360), -350.0)
    assert isclose(modulo(-30, -360), -330.0)
    assert isclose(modulo(-0, -360), 0.0)
    assert isclose(modulo(360, -360), 0.0)
