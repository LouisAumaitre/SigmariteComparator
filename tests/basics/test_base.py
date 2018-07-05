import math

from sigmar.basics.base import infantry


def test_base_surface():
    # assert
    assert infantry.surface() == math.pi * 25 * 25
