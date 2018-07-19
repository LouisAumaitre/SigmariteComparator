import math

from sigmar.basics.base import infantry_base


def test_base_surface():
    # assert
    assert infantry_base.surface() == math.pi * 25 * 25
