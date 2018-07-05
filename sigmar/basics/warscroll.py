from typing import Union, List

from copy import copy

from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.weapon import Weapon


def weapon_choice_name(weapon_list: List[Union[Weapon, Rule]]) -> str:
    new_list = []
    for item in weapon_list:
        if item.name not in new_list:
            new_list.append(item.name)
    return str(new_list)[1:-1].replace('\'', '')


class Warscroll:
    def __init__(
            self,
            name: str,
            weapon_options: List[List[Union[Weapon, Rule]]],
            *args,
            **kwargs
    ):
        self.units = {
            weapon_choice_name(weapons_and_rules): Unit(
                name, [w for w in weapons_and_rules if isinstance(w, Weapon)], *args, **kwargs
            ) for weapons_and_rules in weapon_options
        }
        self.name = name

    def average_damage(self, armour: Roll, data: dict, _range=1, front_size=1000, nb=None):
        return {key: unit.average_damage(armour, data, _range, front_size, nb) for key, unit in self.units.items()}

    def average_health(self, rend=0):
        return {key: unit.average_health(rend) for key, unit in self.units.items()}

    def stats(self, armour: Roll, data: dict, rend=0, _range=1, front_size=1000, nb=None):
        return {key: (
            unit.average_damage(armour, data, _range, front_size, nb), unit.average_health(rend)
        ) for key, unit in self.units.items()}

    def simplest_stats(self, armour: Roll, data: dict, rend=0, _range=1, front_size=1000, nb=None):
        for k, v in self.units.items():
            numbers = v.size if nb is None else nb
            numbers = f'{numbers} ' if numbers > 1 else ''
            print(f'{numbers}{v.name} with {k}: '
                  f'{int(round(v.average_damage(armour, copy(data), _range, front_size, nb) * 10))}'
                  f'/{int(round(v.average_health(rend, nb)))} {v.describe_formation(data, _range, front_size, nb)}')
