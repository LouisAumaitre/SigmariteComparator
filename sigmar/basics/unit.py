from typing import Union, List

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.rules import Rule
from sigmar.basics.weapon import Weapon


class Unit:
    def __init__(
            self,
            name: str,
            weapons: Union[List[Weapon]],
            move: Union[int, str, RandomValue],
            save: int,
            bravery: int,
            wounds: int,
            rules: List[Rule],
            keywords: List[str],
    ):
        self.name = name
        self.weapons = weapons
        self.move = rv(move)
        self.save = save
        self.bravery = bravery
        self.wounds = wounds
        self.keywords = keywords
        self.reroll_save = 0

        self.rules = rules
        for r in self.rules:
            r.apply(self)

    def average_damage(self, armour=4, range=1):
        return sum([w.average_damage(armour, range) for w in self.weapons if isinstance(w, Weapon)])

    def chances_to_save(self, rend):
        chances = (7 - (self.save + rend)) / 6
        chances *= 1 + min(self.reroll_save, (self.save + rend) - 1) / 6
        return chances

    def average_health(self, rend=0):
        save = self.chances_to_save(rend)
        return self.wounds / (1 - save)


class WeaponRule(Rule):
    def apply(self, item):
        if isinstance(item, Weapon):
            self.effect(item)
        elif isinstance(item, Unit):
            self.apply(item.weapons)
        elif isinstance(item, list):
            for i in item:
                self.apply(i)
