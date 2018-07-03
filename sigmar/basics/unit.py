from typing import Union, List

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.rules import Rule
from sigmar.basics.weapon import Weapon


class Unit:
    def __init__(
            self,
            name: str,
            weapon_options: Union[List[Weapon, Rule], List[List[Weapon, Rule]]],
            move: Union[int, str, RandomValue],
            save: int,
            bravery: int,
            wounds: int,
            rules: List[Rule],
    ):
        self.name = name
        self.weapon_options = weapon_options
        self.move = rv(move)
        self.save = save
        self.bravery = bravery
        self.wounds = wounds
        self.reroll_save = 0

        self.rules = rules
        for r in self.rules:
            r.apply(self)

    def average_damage(self, armour=4):
        if isinstance(self.weapon_options[0], Weapon):
            return [sum([w.average_damage(armour) for w in self.weapon_options if isinstance(w, Weapon)])]
        else:
            return [sum(
                [w.average_damage(armour) for w in weapon_list if isinstance(w, Weapon)]
            ) for weapon_list in self.weapon_options]
