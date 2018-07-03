from typing import Union, List

from sigmar.basics.random_value import RandomValue
from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.weapon import Weapon


def weapon_choice_name(weapon_list: List[Union[Weapon, Rule]]) -> str:
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
        self.units = {
            weapon_choice_name(weapons_and_rules): Unit(
                name,
                [w for w in weapons_and_rules if isinstance(w, Weapon)],
                move, save, bravery, wounds,
                [*rules, *[r for r in weapons_and_rules if isinstance(r, Rule)]],
                keywords) for weapons_and_rules in weapon_options
        }
        self.name = name

    def average_damage(self, armour=4):
        return {key: unit.average_damage(armour) for key, unit in self.units.items()}

    def average_health(self, rend=0):
        return {key: unit.average_health(rend) for key, unit in self.units.items()}

    def stats(self, armour=4, rend=0):
        return {key: (unit.average_damage(armour), unit.average_health(rend)) for key, unit in self.units.items()}

    def simplest_stats(self, armour=4, rend=0):
        for k, v in self.units.items():
            print(f'{v.name} with {k}: {int(round(v.average_damage(armour) * 10))}/{int(round(v.average_health(rend)))}')
