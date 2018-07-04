from typing import Union, List

from copy import copy

from sigmar.basics.base import Base
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
            base: Base,
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
        self.base = base
        self.keywords = keywords
        self.ignores_1_rend = False

        self.rules = rules
        for r in self.rules:
            r.apply(self)

    def formation(self, data: dict, front_size, nb):
        if nb is None:
            nb = self.size
        data[SELF_NUMBERS] = nb
        rows = []
        while nb > 0:
            row = max(min(front_size // self.base.width, nb), 1)
            rows.append(row)
            nb -= row
        return rows

    def describe_formation(self, data: dict, _range, front_size, nb):
        rows = self.formation(data, front_size, nb)
        attacking = 0
        for row in rows:
            if sum([w.average_damage(Roll(4), copy(data), _range) for w in self.weapons if isinstance(w, Weapon)]):
                attacking += row
            else:
                break
            _range += self.base.depth / 25.6
        return f'{rows[0]}x{len(rows)} ({attacking} attacking)'

    def average_damage(self, armour: Roll, data: dict, _range=0, front_size=1000, nb=None):
        total = 0
        for row in self.formation(data, front_size, nb):
            total += row * sum(
                [w.average_damage(armour, copy(data), _range) for w in self.weapons if isinstance(w, Weapon)]
            )
            _range += self.base.depth / 25.6
        return total

    def average_health(self, rend=0, nb=None):
        if nb is None:
            nb = self.size
        if self.ignores_1_rend and rend == -1:
            rend = 0
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
