from typing import Union, List, Callable

from sigmar.basics.string_constants import WEAPON_RANGE, SELF_BASE, ENEMY_BASE, ENEMY_NUMBERS, INCH


class RandomValue:
    defined_value: Union[str, int] = 0

    def __init__(self, defined_value: Union[str, int]):
        self.defined_value = defined_value
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod and extra_ignore

    def average(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(context)
            mod += add_mod

        return self._average(context) + mod

    def _average(self, context: dict):
        if isinstance(self.defined_value, int):
            return self.defined_value
        elif self.defined_value == 'D6':
            return 3.5
        elif self.defined_value == '2D6':
            return 7
        elif self.defined_value == 'all_in_range':
            swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
            hits = swing * 2 / context[ENEMY_BASE].width + 1
            hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
            return max(1, min(hits, context[ENEMY_NUMBERS]))
        else:
            return 0

    def max(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(context)
            mod += add_mod

        return self._max(context) + mod

    def _max(self, context: dict):

        if isinstance(self.defined_value, int):
            return self.defined_value
        elif self.defined_value == 'D6':
            return 6
        elif self.defined_value == '2D6':
            return 12
        elif self.defined_value == 'all_in_range':
            swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
            hits = swing * 2 / context[ENEMY_BASE].width + 1
            hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
            return max(1, min(hits, context[ENEMY_NUMBERS]))
        else:
            return 0


def rv(defined_value: Union[str, int, RandomValue]):
    if isinstance(defined_value, RandomValue):
        return defined_value
    return RandomValue(defined_value)
