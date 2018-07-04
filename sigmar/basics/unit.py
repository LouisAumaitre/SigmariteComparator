from typing import Union, List

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import SELF_NUMBERS
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
            min_size: int,
            base_size: int,  # mm
            rules: List[Rule],
            keywords: List[str],
    ):
        self.name = name
        self.weapons = weapons
        self.move = rv(move)
        self.save = Roll(save)
        self.bravery = bravery
        self.wounds = wounds
        self.min_size = min_size
        self.size = min_size
        self.base_size = base_size
        self.keywords = keywords

        self.rules = rules
        for r in self.rules:
            r.apply(self)

    def average_damage(self, armour: Roll, data: dict, _range=0, front_size=1000, nb=None):
        if nb is None:
            nb = self.size
        data[SELF_NUMBERS] = nb
        rows = []
        while nb > 0:
            row = max(min(front_size // self.base_size, nb), 1)
            rows.append(row)
            nb -= row

        total = 0
        for row in rows:
            total += sum([w.average_damage(armour, data, _range) for w in self.weapons if isinstance(w, Weapon)]) * row
            _range += self.base_size / 25.6
        return total

    def average_health(self, rend=0, nb=None):
        if nb is None:
            nb = self.size
        save, crit = self.save.chances({}, mod=rend)
        save += crit
        return nb * self.wounds / (1 - save)


class WeaponRule(Rule):
    def apply(self, item):
        if isinstance(item, Weapon):
            self.effect(item)
        elif isinstance(item, Unit):
            self.apply(item.weapons)
        elif isinstance(item, list):
            for i in item:
                self.apply(i)
