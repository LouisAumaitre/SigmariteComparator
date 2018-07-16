from typing import Union, List

from copy import copy

from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import SELF_WOUNDS, RANGE
from sigmar.basics.unit import Unit
from sigmar.basics.weapon import Weapon


def weapon_choice_name(weapon_list: List[Union[Weapon, Rule]]) -> str:
    new_list = []
    for item in weapon_list:
        if item.name not in new_list:
            new_list.append(item.name)
    return str(new_list)[1:-1].replace('\'', '')


def selective_weapon_choice_name(
        weapon_list: List[Union[Weapon, Rule]],
        all_choices: List[List[Union[Weapon, Rule]]]
) -> str:
    new_list = []
    for item in weapon_list:
        if all([item.name in [i.name for i in choice] for choice in all_choices]):
            continue

        if item.name not in new_list:
            new_list.append(item.name)
    return str(new_list)[1:-1].replace('\'', '')


class Warscroll:
    def __init__(
            self,
            name: str,
            weapon_options: List[List[Union[Weapon, Rule]]],
            *args,
            rules: List[Rule],
            **kwargs
    ):
        self.units = {
            selective_weapon_choice_name(weapons_and_rules, weapon_options): Unit(
                name,
                [w for w in weapons_and_rules if isinstance(w, Weapon)],
                *args,
                rules=[*rules, *[r for r in weapons_and_rules if isinstance(r, Rule)]],
                **kwargs
            ) for weapons_and_rules in weapon_options
        }
        self.name = name

    def average_damage(self, armour: Roll, data: dict, front_size=1000, nb=None):
        return {key: unit.average_damage(armour, data, front_size, nb) for key, unit in self.units.items()}

    def average_health(self, context):
        return {key: unit.average_health(context) for key, unit in self.units.items()}

    def stats(self, armour: Roll, context: dict, front_size=1000, nb=None):
        return {key: (
            unit.average_damage(armour, context, front_size, nb), unit.average_health(context)
        ) for key, unit in self.units.items()}

    def simplest_stats(self, armour: Roll, context: dict, front_size=1000, nb=None):
        for k, v in self.units.items():
            numbers = v.size if nb is None else nb
            numbers = f'{numbers} ' if numbers > 1 else ''
            health = context.get(SELF_WOUNDS, v.wounds)
            health = f' ({health}/{v.wounds})' if health != v.wounds else ''
            equip = f' with {k}' if len(self.units) > 1 else ''
            ranged_context = copy(context)
            ranged_context[RANGE] = max(3.01, context.get(RANGE, 0))
            ranged = f'{int(round(v.average_damage(armour, ranged_context, front_size, nb) * 10))}/'
            ranged = '' if ranged == '0/' else ranged
            flight = 'F' if v.can_fly else ''
            print(
                f'{numbers}{v.name}{health}{equip}: '
                f'{ranged}'
                f'{int(round(v.average_damage(armour, copy(context), front_size, nb) * 10))}'
                f'/{int(round(v.average_health(context, nb)))} '
                f'{v.describe_formation(context, front_size, nb)} '
                f'M{v.speed_grade(context)}{flight}')
