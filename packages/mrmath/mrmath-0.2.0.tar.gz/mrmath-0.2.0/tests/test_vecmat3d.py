"""
Test for the module mod:`mrmath.vecmat3d`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>
"""

from math import isclose, pi, sqrt, acos

import numpy
import pytest
from mrmath.vecmat3d import Vec3D


def test_nullvec() -> None:
    """Nullvektor."""
    nullvector = Vec3D()
    nullvector == Vec3D([0, 0, 0])


def test_init() -> None:
    """initialisierung."""
    _ = Vec3D()
    _ = Vec3D((1, 2, 3))
    _ = Vec3D([1, 2, 3])
    _ = Vec3D(theta=pi / 2, phi=pi / 2, r=1)
    with pytest.raises(TypeError):
        _ = Vec3D((1, 2, 3, 4))


def test_init_polar_01() -> None:
    """initialisierung."""
    vector = Vec3D(phi=pi / 4, theta=0, r=sqrt(2))
    assert isclose(vector.x, 1)
    assert isclose(vector.y, 1)
    assert isclose(vector.z, 0)


def test_init_polar_02() -> None:
    """initialisierung."""
    vector = Vec3D(phi=-pi / 4, theta=0, r=sqrt(2))
    assert isclose(vector.x, 1)
    assert isclose(vector.y, -1)
    assert isclose(vector.z, 0)


def test_init_polar_03() -> None:
    """initialisierung."""
    vector = Vec3D(phi=3 * pi / 4, theta=0, r=sqrt(2))
    assert isclose(vector.x, -1)
    assert isclose(vector.y, 1)
    assert isclose(vector.z, 0)


def test_init_polar_04() -> None:
    """initialisierung."""
    vector = Vec3D(phi=5 * pi / 4, theta=0, r=sqrt(2))
    assert isclose(vector.x, -1)
    assert isclose(vector.y, -1)
    assert isclose(vector.z, 0)


def test_init_polar_05() -> None:
    """initialisierung."""
    vector = Vec3D(phi=7 * pi / 4, theta=0, r=sqrt(2))
    assert isclose(vector.x, 1)
    assert isclose(vector.y, -1)
    assert isclose(vector.z, 0)


def test_init_polar_06() -> None:
    """initialisierung."""
    with pytest.raises(TypeError):
        _ = Vec3D(phi=0, theta=1, r='test')
    with pytest.raises(TypeError):
        _ = Vec3D(phi=0, theta='test', r=2)
    with pytest.raises(TypeError):
        _ = Vec3D(phi='test', theta=1, r=3)


def test_init_polar_07() -> None:
    """initialisierung."""
    vector = Vec3D(az=pi / 4, elev=0, r=sqrt(2))
    assert isclose(vector.x, 1)
    assert isclose(vector.y, 1)
    assert isclose(vector.z, 0)


def test_init_polar_08() -> None:
    """initialisierung."""
    vector = Vec3D(az=pi / 4, elev=pi / 4)
    assert isclose(vector.x, 0.5)
    assert isclose(vector.y, 0.5)
    assert isclose(vector.z, 1 / sqrt(2))


def test_init_polar_09() -> None:
    """initialisierung."""
    with pytest.raises(TypeError):
        _ = Vec3D(az=0, elev='test', r=3)
    with pytest.raises(TypeError):
        _ = Vec3D(az='test', elev=1, r=5)
    with pytest.raises(TypeError):
        _ = Vec3D(az=0, elev=1, r='test')


def test_xyz_01() -> None:
    """propertys: x, y, z."""
    vector = Vec3D()
    vector.x = 9.9
    vector.y = 5
    vector.z = 1.1
    assert vector == Vec3D([9.9, 5, 1.1])
    assert vector.x == 9.9
    assert vector.y == 5
    assert vector.z == 1.1


def test_xyz_02() -> None:
    """propertys: x, y, z."""
    vector = Vec3D()
    with pytest.raises(TypeError):
        vector.x = 'string'
    with pytest.raises(TypeError):
        vector.y = 'string'
    with pytest.raises(TypeError):
        vector.z = 'string'


def test_xyz() -> None:
    """property: xyz."""
    vec = Vec3D()
    assert isinstance(vec.xyz, list)
    assert len(vec.xyz) == 3


def test_polar_01() -> None:
    """property: polar."""
    polar_vector = Vec3D((1, 1, 1)).polar
    assert isclose(polar_vector[0], pi / 4)
    assert isclose(polar_vector[1], acos(sqrt(2) / sqrt(3)))
    assert isclose(polar_vector[2], sqrt(3))
    assert isclose(polar_vector[0], Vec3D([1, 1, 1]).phi)
    assert isclose(polar_vector[1], Vec3D([1, 1, 1]).theta)
    assert isclose(polar_vector[2], Vec3D([1, 1, 1]).r)


def test_polar_02() -> None:
    """property: polar."""
    vector = Vec3D((0, 0, 1))
    assert vector.phi == 0.0


def test_polar_03() -> None:
    """property: polar."""
    vector = Vec3D((-1, -1, 1))
    assert vector.phi == 5 * pi / 4


def test_polar_04() -> None:
    """property: polar."""
    vector = Vec3D()
    vector.x = 0
    vector.y = 0
    vector.z = 0
    assert isclose(vector.theta, 0.0)


def test_array() -> None:
    """property: ``array``."""
    vector = Vec3D((3, 7, 9))
    assert isinstance(vector.array, numpy.ndarray)
    assert len(vector.array) == 3


def test__abs() -> None:
    """macig: ``__abs__``."""
    vector = Vec3D((1, 1, 1))
    assert isclose(abs(vector), sqrt(3))


def test__getitem_01() -> None:
    """macig: ``__getitem__``."""
    vector = Vec3D((3, 7, 13))
    assert vector[0] == vector.x
    assert vector[1] == vector.y
    assert vector[2] == vector.z


def test__getitem_02() -> None:
    """macig: ``__getitem__``."""
    vector = Vec3D((3, 7, 13))
    with pytest.raises(IndexError):
        _ = vector[4]


def test__setitem() -> None:
    """macig: ``__getitem__``."""
    vector = Vec3D()
    vector[0] = 3
    vector[1] = 5
    vector[2] = 7
    assert vector.x == 3
    assert vector.y == 5
    assert vector.z == 7
    with pytest.raises(IndexError):
        vector[3] = 13


def test__repr() -> None:
    """macig: ``__repr__``."""
    vector = Vec3D()
    assert repr(vector) == 'Vec3D([0, 0, 0])'


def test__neg() -> None:
    """macig: ``__neg__``."""
    vector = Vec3D((5, -4.3, 0.99))
    vector_neg = -vector
    assert isclose(vector_neg.x, -5)
    assert isclose(vector_neg.y, 4.3)
    assert isclose(vector_neg.z, -0.99)


def test__add() -> None:
    """macig: ``__add__``."""
    vector1 = Vec3D()
    vector2 = Vec3D((1, 2, 3))
    assert vector1 + vector2 == vector2
    assert vector1 + 4 == Vec3D((4, 4, 4))
    assert vector2 + 5.1 == Vec3D((6.1, 7.1, 8.1))
    with pytest.raises(TypeError):
        _ = vector1 + [0, 1, 2]


def test__radd() -> None:
    """macig: ``__radd__``."""
    vector1 = Vec3D()
    vector2 = Vec3D((1, 2, 3))
    assert vector1 + vector2 == vector2
    assert 4 + vector1 == Vec3D((4, 4, 4))
    assert 5.1 + vector2 == Vec3D((6.1, 7.1, 8.1))
    with pytest.raises(TypeError):
        _ = [0, 1, 2] + vector1


def test__iadd() -> None:
    """macig: ``__iadd__``."""
    vector1 = Vec3D()
    vector2 = Vec3D((1, 2, 3))
    vector1 += vector2
    assert vector1 == vector2
    vector1 = Vec3D()
    vector1 += 4
    assert vector1 == Vec3D((4, 4, 4))
    vector2 = Vec3D((1, 2, 3))
    vector2 += 5.1
    assert vector2 == Vec3D((6.1, 7.1, 8.1))
    with pytest.raises(TypeError):
        vector1 += [0, 1, 2]


def test__truediv() -> None:
    """macig: ``__truediv__``."""
    dividend = Vec3D([1, 2, 3])
    quotient = dividend / 2
    assert quotient == Vec3D([0.5, 1.0, 1.5])
    with pytest.raises(TypeError):
        quotient = dividend / 'string'


def test__itruediv() -> None:
    """macig: ``__itruediv__``."""
    quotient = Vec3D([1, 2, 3])
    quotient /= 2
    assert quotient == Vec3D([0.5, 1.0, 1.5])

    quotient = Vec3D([2, 3, 5])
    quotient /= 2.0
    assert quotient == Vec3D([1.0, 1.5, 2.5])

    quotient = Vec3D([1.0, 2.0, 3.4])
    quotient /= 2
    assert quotient == Vec3D([0.5, 1.0, 1.7])

    quotient = Vec3D([2.4, 3.3, 5.5])
    quotient /= 2.2
    assert isclose(quotient.x, 1.090909090909)
    assert isclose(quotient.y, 1.5)
    assert isclose(quotient.z, 2.5)

    with pytest.raises(TypeError):
        quotient /= 'string'


def test__eq() -> None:
    """macig: ``__eq__``."""
    assert (Vec3D([1, 2, 3]) == Vec3D([1, 2, 3])) == True   # noqa: E712
    assert (Vec3D([1, 2, 3]) == Vec3D([3, 2, 1])) == False   # noqa: E712
    assert (Vec3D([1, 2, 3]) == 3) == False   # noqa: E712
