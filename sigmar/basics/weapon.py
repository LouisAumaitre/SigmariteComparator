from typing import List, Union, Tuple

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule


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
        self.rules = rules

        self.rules = rules
        for r in rules:
            r.apply(self)

    def average_hits(self, dices) -> Tuple[float, float]:
        return self.tohit.average(dices)

    def average_wounds(self, dices) -> Tuple[float, float]:
        return self.towound.average(dices)

    def unsaved_chances(self, armour: Roll) -> float:
        chances, _ = armour.chances(mod=self.rend)
        return 1 - chances

    def average_damage(self, armour: Roll, _range=1):
        if _range > self.range:
            return 0
        attacks = self.attacks.average()
        hits, critic_hits = self.average_hits(attacks)
        wounds, critic_wounds = self.average_wounds(hits)
        unsaved = wounds * self.unsaved_chances(armour)
        damage = unsaved * self.wounds.average()
        return damage
