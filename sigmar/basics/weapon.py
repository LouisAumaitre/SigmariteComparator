from typing import List, Union, Tuple, Callable

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import TOWOUND_MOD_ON_CRIT_HIT, BONUS_REND, CRIT_BONUS_REND


class Weapon:
    def __init__(
            self,
            name: str,
            range: int,
            attacks: Union[int, str, RandomValue],
            tohit,
            towound,
            rend,
            wounds: Union[int, str, RandomValue],
            rules: List[Rule],
    ):
        self.name = name
        self.range = range
        self.attacks = rv(attacks)
        self.tohit = Roll(tohit)
        self.towound = Roll(towound)
        self.rend = rend
        self.wounds = rv(wounds)

        self.tohit_critical: List[Callable] = []
        self.towound_critical: List[Callable] = []

        self.rules = rules
        for r in rules:
            r.apply(self)

    def average_hits(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.tohit.average(dices, extra_data, mod)

    def average_wounds(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.towound.average(dices, extra_data, mod)

    def unsaved_chances(self, armour: Roll, extra_rend=0) -> float:
        chances, _ = armour.chances({}, mod=self.rend + extra_rend)
        return 1 - chances

    def average_damage(self, armour: Roll, data: dict, _range=1):
        if _range > self.range:
            return 0
        mortal_wounds = 0

        attacks = self.attacks.average(data)
        hits, critic_hits = self.average_hits(attacks, data)

        wounds, critic_wounds = self.average_wounds(hits, data)
        _wounds, _critic_wounds = self.average_wounds(critic_hits, data, mod=data.get(TOWOUND_MOD_ON_CRIT_HIT, 0))
        wounds += _wounds
        critic_wounds += _critic_wounds

        unsaved = wounds * self.unsaved_chances(armour, extra_rend=data.get(BONUS_REND, 0))
        unsaved += critic_wounds * self.unsaved_chances(
            armour, extra_rend=data.get(BONUS_REND, 0) + data.get(CRIT_BONUS_REND, 0))
        damage = unsaved * self.wounds.average(data) + mortal_wounds
        return damage
