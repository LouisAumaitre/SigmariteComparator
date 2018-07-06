from typing import Union, List, Callable, Dict, Any

from sigmar.basics.string_constants import WEAPON_RANGE, SELF_BASE, ENEMY_BASE, ENEMY_NUMBERS, INCH, SELF_WOUNDS


class Value:
    def __init__(self):
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod

    def average(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod = bonus(context)
            mod += add_mod

        return self._average(context) + mod

    def _average(self, context: dict):
        raise NotImplementedError

    def max(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod = bonus(context)
            mod += add_mod

        return self._max(context) + mod

    def _max(self, context: dict):
        raise NotImplementedError


class RandomMultValue(Value):
    def __init__(self, average_mult, max_mult, base_value: Value):
        Value.__init__(self)
        self.average_mult = average_mult
        self.max_mult = max_mult
        self.base_value = base_value

    def average(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod = bonus(context)
            mod += add_mod

        return self._average(context, mod)

    def _average(self, context: dict, mod=0):
        return self.average_mult * self.base_value.average(context, mod)

    def max(self, context: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod = bonus(context)
            mod += add_mod

        return self._max(context, mod)

    def _max(self, context: dict, mod=0):
        return self.max_mult * self.base_value.max(context, mod)


class FixedValue(Value):
    def __init__(self, defined_value):
        Value.__init__(self)
        self.defined_value = defined_value

    def _average(self, context: dict):
        return self.defined_value

    def _max(self, context: dict):
        return self.defined_value


class DiceValue(Value):
    def __init__(self, defined_value: str):
        Value.__init__(self)
        self.defined_value = defined_value

    def _average(self, context: dict):
        if self.defined_value == 'D6':
            return 3.5
        elif self.defined_value == '2D6':
            return 7
        elif self.defined_value == 'D3':
            return 2
        elif self.defined_value == 'all_in_range':
            swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
            hits = swing * 2 / context[ENEMY_BASE].width + 1
            hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
            return max(1, min(hits, context[ENEMY_NUMBERS]))
        else:
            return 0

    def _max(self, context: dict):
        if self.defined_value == 'D6':
            return 6
        elif self.defined_value == '2D6':
            return 12
        elif self.defined_value == 'D3':
            return 3
        elif self.defined_value == 'all_in_range':
            swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
            hits = swing * 2 / context[ENEMY_BASE].width + 1
            hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
            return max(1, min(hits, context[ENEMY_NUMBERS]))
        else:
            return 0


def _value(defined_value: Union[str, int, Value]):
    if isinstance(defined_value, Value):
        return defined_value
    if isinstance(defined_value, int):
        return FixedValue(defined_value)
    return DiceValue(defined_value)


class MonsterValue(Value):
    def __init__(self, values: Dict[int, Union[str, int, Value]]):
        Value.__init__(self)
        self.defined_value = {k: _value(v) for k, v in values.items()}

    def _average(self, context: dict):
        if SELF_WOUNDS in context:
            possible = [key for key in self.defined_value.keys() if key <= context[SELF_WOUNDS]]
            return self.defined_value[max(possible)].average(context, 0)
        return self.defined_value[max(self.defined_value.keys())].average(context, 0)

    def _max(self, context: dict):
        if SELF_WOUNDS in context:
            possible = [key for key in self.defined_value.keys() if key <= context[SELF_WOUNDS]]
            return self.defined_value[max(possible)].max(context, 0)
        return self.defined_value[max(self.defined_value.keys())].max(context, 0)


def value(defined_value: Union[str, int, Value, Dict[int, Union[str, int, Value]]]):
    if isinstance(defined_value, Value):
        return defined_value
    if isinstance(defined_value, int):
        return FixedValue(defined_value)
    if isinstance(defined_value, dict):
        return MonsterValue(defined_value)
    return DiceValue(defined_value)
