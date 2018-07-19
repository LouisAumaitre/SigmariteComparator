from typing import List, Union, Tuple, Callable, Dict

from math import factorial

from copy import copy

from sigmar.basics.attack_round import attack_round_computer
from sigmar.basics.value import Value, value
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import (
    WEAPON_RANGE,
    RANGE,
    ENEMY_SAVE,
)


class Weapon:
    def __init__(
            self,
            name: str,
            range_: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            attacks: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            tohit,
            towound,
            rend,
            wounds: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            rules: List[Rule],
    ):
        self.name = name
        self.range = value(range_)
        self.attacks = value(attacks)
        self.tohit = Roll(tohit)
        self.towound = Roll(towound)
        self.rend = value(rend)
        self.wounds = value(wounds)

        self.attack_rules: List[Callable] = []

        self.rules = rules
        for r in rules:
            r.apply(self)

    def average_hits(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.tohit.average(dices, extra_data, mod)

    def average_wounds(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.towound.average(dices, extra_data, mod)

    def unsaved_chances(self, extra_data: dict, extra_rend=0) -> float:
        chances, crit = extra_data[ENEMY_SAVE].chances({}, mod=self.rend.average(extra_data, extra_rend))
        return 1 - chances - crit

    def average_damage(self, context: dict):
        if context.get(RANGE, 0) > self.range.average(context)\
                or self.range.average(context) > 3 >= context.get(RANGE, 0):
            return 0
        context[WEAPON_RANGE] = self.range.average(context)
        dmg = attack_round_computer(
            self.attacks, self.tohit, self.towound, self.rend, self.wounds, self.attack_rules, copy(context))
        return sum([e['damage'] * e['proba'] for e in dmg])


def binomial(n, k):
    # combinations of k in n
    return factorial(n) / (factorial(k) * factorial(n - k))
