from typing import Union, List

from sigmar.basics.random_value import RandomValue, rv
from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.weapon import Weapon


def weapon_choice_name(weapon_list: List[Union[Weapon, Rule]]):
    return str([item.name for item in weapon_list])[1:-1]


class Warscroll:
    def __init__(
            self,
            name: str,
            weapon_options: List[List[Union[Weapon, Rule]]],
            move: Union[int, str, RandomValue],
            save: int,
            bravery: int,
            wounds: int,
            rules: List[Rule],
            keywords: List[str],
    ):
        self.units = [
            Unit(name, weapons, move, save, bravery, wounds, rules, keywords) for weapons in weapon_options
        ]
        self.name = name

    def average_damage(self, armour=4):
        return {weapon_choice_name(unit.weapons): unit.average_damage(armour) for unit in self.units}
