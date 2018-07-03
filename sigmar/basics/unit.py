from typing import Union, List

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.rules import Rule
from sigmar.basics.weapon import Weapon


def weapon_choice_name(weapon_list: List[Union[Weapon, Rule]]):
    return str([item.name for item in weapon_list])[1:-1]


class Unit:
    def __init__(
            self,
            name: str,
            weapon_options: Union[List[Union[Weapon, Rule]], List[List[Union[Weapon, Rule]]]],
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
            return {
                weapon_choice_name(self.weapon_options): sum([
                    w.average_damage(armour) for w in self.weapon_options if isinstance(w, Weapon)
                ])
            }
        else:
            return {
                weapon_choice_name(weapon_list): sum(
                    [w.average_damage(armour) for w in weapon_list if isinstance(w, Weapon)]
                ) for weapon_list in self.weapon_options
            }
