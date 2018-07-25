from typing import Union, List, Callable, Dict

from sigmar.basics.string_constants import WEAPON_RANGE, SELF_BASE, ENEMY_BASE, ENEMY_NUMBERS, INCH, SELF_WOUNDS, \
    SELF_MOVE, DID_MOVE


class Value:
    def __init__(self):
        self.rules: List[Callable] = []  # function take dict, return mod

    def average(self, context: dict, mod=0):
        mod = value(mod)
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        if isinstance(mod, FixedValue) and mod.defined_value == 0:
            return self._average(context)
        return self._average(context) + mod.average(context)

    def _average(self, context: dict):
        raise NotImplementedError

    def max(self, context: dict, mod=0):
        mod = value(mod)
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        if isinstance(mod, FixedValue) and mod.defined_value == 0:
            return self._max(context)
        return self._max(context) + mod.max(context)

    def _max(self, context: dict):
        raise NotImplementedError

    def potential_values(self, context: dict, mod=0):
        mod = value(mod)
        for bonus in self.rules:
            add_mod = bonus(context)
            mod += add_mod

        if isinstance(mod, FixedValue) and mod.defined_value == 0:
            return [(potential, proba) for (potential, proba) in self._potential_values(context)]
        return [(potential + potential_mod, proba * proba_mod)
                for (potential, proba) in self._potential_values(context)
                for (potential_mod, proba_mod) in mod.potential_values(context)]

    def _potential_values(self, context: dict):
        raise NotImplementedError

    def __add__(self, other):
        if other == 0:
            return self
        return SumValue(self, value(other))

    def __mul__(self, other):
        if other == 1:
            return self
        if self == 1:
            return value(other)
        if other == 0:
            return FixedValue(0)
        return MultValue(self, value(other))

    def __sub__(self, other):
        if other == 0:
            return self
        return SumValue(self, MultValue(FixedValue(-1), value(other)))


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

    def __str__(self):
        return f'|{self.val_1}+{self.val_2}|'


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

    def __str__(self):
        return f'|{self.val_1}*{self.val_2}|'


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

    def __str__(self):
        short_probas = [(f'{int(round(v, 2) * 100)}%', k) for k, v in self.probas.items()]
        return f'|R{short_probas}|'


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

    def __str__(self):
        return f'|{self.defined_value}|'

    def __eq__(self, other):
        if other == self.defined_value or (isinstance(other, FixedValue) and other.defined_value == self.defined_value):
            return True
        return False


class DiceValue(Value):
    def __init__(self, defined_value: int):
        Value.__init__(self)
        self.defined_value = defined_value

    def _average(self, context: dict):
        return sum([i + 1 for i in range(self.defined_value)]) / self.defined_value

    def _max(self, context: dict):
        return self.defined_value

    def _potential_values(self, context: dict):
        return [(i + 1, 1/self.defined_value) for i in range(self.defined_value)]

    def __str__(self):
        return f'|D{self.defined_value}|'


class AllInRangeValue(Value):

    def _average(self, context: dict):
        swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
        hits = swing * 2 / context[ENEMY_BASE].width + 1
        hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
        return max(1, min(hits, context[ENEMY_NUMBERS]))

    def _max(self, context: dict):
        swing = context[WEAPON_RANGE] * INCH + context[SELF_BASE].width
        hits = swing * 2 / context[ENEMY_BASE].width + 1
        hits += max(0, context[WEAPON_RANGE] * INCH - context[ENEMY_BASE].depth) / context[ENEMY_BASE].width
        return max(1, min(hits, context[ENEMY_NUMBERS]))

    def _potential_values(self, context: dict):
        m = int(self.max(context))
        return [(i + 1, 1/m) for i in range(m)]


class MoveAcrossValue(Value):
    def _average(self, context: dict):
        if not context.get(DID_MOVE, True):
            return 0
        return context.get(SELF_MOVE, 0) // 2

    def _max(self, context: dict):
        if not context.get(DID_MOVE, True):
            return 0
        return context.get(SELF_MOVE, 0) // 2

    def _potential_values(self, context: dict):
        if not context.get(DID_MOVE, True):
            return 0
        return [(context.get(SELF_MOVE, 0) // 2, 1)]


def make_dice_value(amount: int, val: int) -> Value:
    if amount == 1:
        return DiceValue(val)
    else:
        return SumValue(make_dice_value(amount - 1, val), DiceValue(val))


def _value(defined_value: Union[str, int, Value]):
    if isinstance(defined_value, Value):
        return defined_value
    if isinstance(defined_value, int):
        return FixedValue(defined_value)
    if isinstance(defined_value, str) and 'D' in defined_value:
        try:
            nb = 1 if defined_value[0] == 'D' else int(defined_value.split('D')[0])
            val = int(defined_value.split('D')[-1])
            return make_dice_value(nb, val)
        except TypeError:
            pass
    if defined_value == 'all_in_range' or defined_value == 'all in range':
        return AllInRangeValue()
    if defined_value == 'move across':
        return MoveAcrossValue()
    raise ValueError(f'{defined_value} is not recognised to define a value')


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

    def __str__(self):
        return f'|M{self.defined_value}|'


def value(defined_value: Union[str, int, Value, Dict[int, Union[str, int, Value]]]):
    if isinstance(defined_value, dict):
        return MonsterValue(defined_value)
    return _value(defined_value)


ONCE_PER_GAME_MULT = 0.15


class OncePerGame(Value):
    def __init__(self, defined_value: Union[str, int, Value]):
        Value.__init__(self)
        self.defined_value = value(defined_value)

    def _average(self, context: dict):
        return self.defined_value.average(context, 0) * ONCE_PER_GAME_MULT

    def _max(self, context: dict):
        return self.defined_value.max(context, 0)

    def _potential_values(self, context: dict):
        possibilities = {
            val: proba * ONCE_PER_GAME_MULT for val, proba in self.defined_value.potential_values(context, 0)}
        possibilities[0] = possibilities.get(0, 0) + 1 - ONCE_PER_GAME_MULT
        return [(val, proba) for val, proba in possibilities.items()]

    def __str__(self):
        return f'|OPG{self.defined_value}|'
