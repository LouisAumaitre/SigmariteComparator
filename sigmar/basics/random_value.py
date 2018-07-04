from typing import Union, List, Callable

import math

from sigmar.basics.string_constants import WEAPON_RANGE, SELF_BASE, ENEMY_BASE, ENEMY_NUMBERS, INCH


class RandomValue:
    defined_value: Union[str, int] = 0

    def __init__(self, defined_value: Union[str, int]):
        self.defined_value = defined_value
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod and extra_ignore

    def average(self, data: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(data)
            mod += add_mod

        if isinstance(self.defined_value, int):
            return self.defined_value + mod
        elif self.defined_value == 'D6':
            return 3.5 + mod
        elif self.defined_value == 'all_in_range':
            swing = data[WEAPON_RANGE] * INCH + data[SELF_BASE].width
            hit_area = (swing * swing * math.pi - data[SELF_BASE].surface()) / 2
            hit_target = hit_area / data[ENEMY_BASE].surface()
            v = max(1, min(hit_target, data[ENEMY_NUMBERS]))
            print(f'swing_surface={swing * swing * 3.14}, base_surface={data[SELF_BASE].surface()},'
                  f'target_surface={data[ENEMY_BASE].surface()}, hit_target={hit_target}, total={v}')
            return v
        else:
            return 0 + mod

    def max(self, data: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(data)
            mod += add_mod

        if isinstance(self.defined_value, int):
            return self.defined_value + mod
        elif self.defined_value == 'D6':
            return 6 + mod
        elif self.defined_value == 'all_in_range':
            hit_area = data[WEAPON_RANGE] * data[WEAPON_RANGE] * 3.14 - data[SELF_BASE].surface()
            hit_target = hit_area / data[ENEMY_BASE].surface()
            return max(1, min(hit_target, data[ENEMY_NUMBERS]))
        else:
            return 0 + mod


def rv(defined_value: Union[str, int, RandomValue]):
    if isinstance(defined_value, RandomValue):
        return defined_value
    return RandomValue(defined_value)
