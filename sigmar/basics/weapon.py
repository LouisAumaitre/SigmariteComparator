from typing import List, Union

from sigmar.basics.random_value import RandomValue, rv
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
        self.tohit = tohit
        self.towound = towound
        self.rend = rend
        self.wounds = rv(wounds)
        self.rules = rules
        self.reroll_tohit, self.reroll_towound = 0, 0

        self.rules = rules
        for r in rules:
            r.apply(self)

    def chances_to_hit(self):
        chances = (7 - self.tohit) / 6
        chances *= 1 + min(self.reroll_tohit, self.tohit - 1) / 6
        return chances

    def chances_to_wound(self):
        chances = (7 - self.towound) / 6
        chances *= 1 + min(self.reroll_towound, self.towound - 1) / 6
        return chances

    def chances_to_pierce_armour(self, armour):
        save = (7 - (armour + self.rend)) / 6
        return 1 - save

    def average_damage(self, armour=4, wounds=1, keywords=[]):
        attacks = self.attacks.average()
        hits = attacks * self.chances_to_hit()
        wounds = hits * self.chances_to_wound()
        unsaved = wounds * self.chances_to_pierce_armour(armour)
        damage = unsaved * self.wounds.average()
        return damage
