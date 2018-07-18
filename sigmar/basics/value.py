from typing import Union, List, Callable, Dict, Any

from sigmar.basics.string_constants import WEAPON_RANGE, SELF_BASE, ENEMY_BASE, ENEMY_NUMBERS, INCH, SELF_WOUNDS


class Value:
    def __init__(self):
        self.rules: List[Callable] = []  # function take dict, return mod

    def average(self, context: dict, mod=0):
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        return self._average(context) + mod

    def _average(self, context: dict):
        raise NotImplementedError

    def max(self, context: dict, mod=0):
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        return self._max(context) + mod

    def _max(self, context: dict):
        raise NotImplementedError

    def potential_values(self, context: dict, mod=0):
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        return [(potential + mod, proba) for (potential, proba) in self._potential_values(context)]

    def _potential_values(self, context: dict):
        raise NotImplementedError

    def __add__(self, other):
        return SumValue(self, value(other))

    def __mul__(self, other):
        return MultValue(self, value(other))


class SumValue(Value):
    def __init__(self, val_1: Value, val_2: Value):
        Value.__init__(self)
        self.val_1 = val_1
        self.val_2 = val_2

    def _average(self, context: dict):
        return self.val_1.average(context) + self.val_2.average(context)

    def _max(self, context: dict):
        return self.val_1.max(context) + self.val_2.max(context)

    def _potential_values(self, context: dict):
        pot_1 = self.val_1.potential_values(context)
        pot_2 = self.val_2.potential_values(context)
        values = [(a + b, p_a * p_b) for (a, p_a) in pot_1 for (b, p_b) in pot_2]
        return [(a, sum([p_b for b, p_b in values if b == a])) for a in set(a for a, _ in values)]


class MultValue(Value):
    def __init__(self, val_1: Value, val_2: Value):
        Value.__init__(self)
        self.val_1 = val_1
        self.val_2 = val_2

    def _average(self, context: dict):
        return self.val_1.average(context) * self.val_2.average(context)

    def _max(self, context: dict):
        return self.val_1.max(context) * self.val_2.max(context)

    def _potential_values(self, context: dict):
        pot_1 = self.val_1.potential_values(context)
        pot_2 = self.val_2.potential_values(context)
        values = [(a * b, p_a * p_b) for (a, p_a) in pot_1 for (b, p_b) in pot_2]
        return [(a, sum([p_b for b, p_b in values if b == a])) for a in set(a for a, _ in values)]


class RandomValue(Value):
    def __init__(self, probas: Dict[int, float]):
        Value.__init__(self)
        self.probas = probas

    def _average(self, context: dict, mod=0):
        return sum([k * v for k, v in self.probas.items()])

    def _max(self, context: dict, mod=0):
        return max(self.probas.keys())

    def _potential_values(self, context: dict, mod=0):
        return [(k, v) for k, v in self.probas.items()]


class FixedValue(Value):
    def __init__(self, defined_value):
        Value.__init__(self)
        self.defined_value = defined_value

    def _average(self, context: dict):
        return self.defined_value

    def _max(self, context: dict):
        return self.defined_value

    def _potential_values(self, context: dict):
        return [(self.defined_value, 1)]


class DiceValue(Value):
    def __init__(self, defined_value: str):
        Value.__init__(self)
        self.defined_value = defined_value

    def _average(self, context: dict):
        if self.defined_value == 'D6':
            return 3.5
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
        elif self.defined_value == 'D3':
            return 3
        elif self.defined_value == 'all_in_range':
            swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
            hits = swing * 2 / context[ENEMY_BASE].width + 1
            hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
            return max(1, min(hits, context[ENEMY_NUMBERS]))
        else:
            return 0

    def _potential_values(self, context: dict):
        if self.defined_value == 'D6':
            return [(i + 1, 1/6) for i in range(6)]
        elif self.defined_value == 'D3':
            return [(i + 1, 1/3) for i in range(3)]
        elif self.defined_value == 'all_in_range':
            return [(self.average(context), 1)]
        else:
            return 0


def _value(defined_value: Union[str, int, Value]):
    if isinstance(defined_value, Value):
        return defined_value
    if isinstance(defined_value, int):
        return FixedValue(defined_value)
    if defined_value == '2D6':
        return SumValue(DiceValue('D6'), DiceValue('D6'))
    if defined_value == '3D6':
        return SumValue(_value('2D6'), DiceValue('D6'))
    if defined_value == '2D3':
        return SumValue(DiceValue('D3'), DiceValue('D3'))
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

    def _potential_values(self, context: dict):
        if SELF_WOUNDS in context:
            possible = [key for key in self.defined_value.keys() if key <= context[SELF_WOUNDS]]
            return self.defined_value[max(possible)].max(context, 0)
        return self.defined_value[max(self.defined_value.keys())].potential_values(context, 0)


def value(defined_value: Union[str, int, Value, Dict[int, Union[str, int, Value]]]):
    if isinstance(defined_value, dict):
        return MonsterValue(defined_value)
    return _value(defined_value)
