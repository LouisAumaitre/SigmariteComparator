from typing import Union, List

from copy import copy

from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import SELF_WOUNDS
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

    def average_health(self, context):
        return {key: unit.average_health(context) for key, unit in self.units.items()}

    def stats(self, armour: Roll, context: dict, _range=1, front_size=1000, nb=None):
        return {key: (
            unit.average_damage(armour, context, _range, front_size, nb), unit.average_health(context)
        ) for key, unit in self.units.items()}

    def simplest_stats(self, armour: Roll, context: dict, _range=1, front_size=1000, nb=None):
        for k, v in self.units.items():
            numbers = v.size if nb is None else nb
            numbers = f'{numbers} ' if numbers > 1 else ''
            health = context.get(SELF_WOUNDS, v.wounds)
            health = f' ({health}/{v.wounds})' if health != v.wounds else ''
            print(
                f'{numbers}{v.name}{health} with {k}: '
                f'{int(round(v.average_damage(armour, copy(context), _range, front_size, nb) * 10))}'
                f'/{int(round(v.average_health(context, nb)))} '
                f'{v.describe_formation(context, _range, front_size, nb)}')
