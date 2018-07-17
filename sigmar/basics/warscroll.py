from typing import Union, List

from copy import copy

from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import SELF_WOUNDS, RANGE
from sigmar.basics.unit import Unit, SpecialUser
from sigmar.basics.weapon import Weapon


def weapon_choice_id(weapon_list: List[Union[Weapon, Rule]]) -> str:
    new_list = []
    for item in weapon_list:
        if item.name not in new_list:
            new_list.append(item.name)
    return str(new_list)[1:-1].replace('\'', '')


def selective_weapon_choice_id(
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


def option_combinations(all_options: List[dict], all_variants, variant_id) -> List[List[dict]]:
    if all_options is None or not len(all_options):
        return [[{}]]
    all_variant_ids = [selective_weapon_choice_id(variant, all_variants) for variant in all_variants]
    option_types = set(option.get('type', 'leader') for option in all_options)
    current_type = list(option_types)[0]

    # combinations without this option
    combinations = option_combinations(
        [o for o in all_options if o.get('type', 'leader') != current_type], all_variants, variant_id
    )
    # combinations with this option
    for version in [opt for opt in all_options if opt.get('type', 'leader') == current_type]:
        version_short_id = option_version_short_id(version, all_options, all_variants)
        if version_short_id not in all_variant_ids or version_short_id == variant_id or current_type != 'leader':
            # leader doesn't pick a different variant than his unit, but can have special weapons
            for sub_combo in option_combinations(
                    [o for o in all_options if o.get('type', 'leader') != current_type], all_variants, variant_id):
                combinations.append([version, *sub_combo])
    return combinations


def option_version_short_id(option, all_options, all_variants):
        special_variant = [*option.get('weapons', []), *option.get('rules', [])]
        special_all_variants = [[
            *_option.get('weapons', []), *_option.get('rules', [])
        ] for _option in all_options if _option.get('type', '') == option.get('type', '')]
        version_id = selective_weapon_choice_id(special_variant, special_all_variants)

        if version_id == '':  # option doesn't have variants
            return selective_weapon_choice_id(special_variant, all_variants)
        return version_id


def option_version_id(option, all_options, all_variants, current_id) -> str:
        version_id = option_version_short_id(option, all_options, all_variants)

        # if option doesn't have variants
        if len([o for o in all_options if o.get('name', '') == option.get('name', '')]) == 1:
            return option.get('name', version_id)
        option_name = option.get('name', '')
        if option_name == '':
            return version_id
        if version_id == current_id:
            return option_name
        return f'{option_name} /w {version_id}'


class Warscroll:
    def __init__(
            self,
            name: str,
            weapon_options: List[List[Union[Weapon, Rule]]],
            *args,
            rules: List[Rule],
            special_options=None,
            **kwargs
    ):
        combinations = [
            {
                'weapons': [w for w in variant if isinstance(w, Weapon)],
                'rules': [*rules, *[r for r in variant if isinstance(r, Rule)]],
                'id': selective_weapon_choice_id(variant, weapon_options),
                'options': option_combo
            } for variant in weapon_options for option_combo in option_combinations(
                special_options, weapon_options, selective_weapon_choice_id(variant, weapon_options)
            )
        ]

        self.units = {}
        for combo in combinations:
            u = Unit(name, combo['weapons'], *args, rules=combo['rules'], **kwargs)
            complete_id = combo['id']
            for o in combo['options']:
                if not len(o):
                    continue
                option_name = o.get('name', '')
                option_id = option_version_id(o, special_options, weapon_options, combo['id'])
                u.special_users.append(SpecialUser(
                    u, option_name,
                    o.get('weapons', []),
                    o.get('rules', []),
                    o.get('max_amount', 1),
                    **{k: v for k, v in kwargs.items() if k not in ['name', 'weapons', 'rules', 'max_amount']}
                ))
                complete_id += ', ' if complete_id != '' else ''
                complete_id += option_id

            self.units[complete_id] = u

        self.name = name

    def average_damage(self, armour: Roll, data: dict, front_size=1000, nb=None):
        return {key: unit.average_damage(armour, data, front_size, nb) for key, unit in self.units.items()}

    def average_health(self, context, nb=None):
        return {key: unit.average_health(context, nb) for key, unit in self.units.items()}

    def stats(self, armour: Roll, context: dict, front_size=1000, nb=None):
        return {key: (
            unit.average_damage(armour, context, front_size, nb), unit.average_health(context)
        ) for key, unit in self.units.items()}

    def simplest_stats(self, context: dict, front_size=1000, nb=None):
        for k, v in self.units.items():
            numbers = v.size if nb is None else nb
            numbers = f'{numbers} ' if numbers > 1 else ''
            health = context.get(SELF_WOUNDS, v.wounds)
            health = f' ({health}/{v.wounds})' if health != v.wounds else ''
            equip = f' with {k}' if k not in [v.name, ''] else ''

            ranged_context = copy(context)
            ranged_context[RANGE] = max(3.01, context.get(RANGE, 0))
            ranged = f'{int(round(v.average_damage(ranged_context, front_size, nb) * 10))}/'
            ranged = '' if ranged == '0/' else ranged
            flight = 'F' if v.can_fly else ''
            print(
                f'{numbers}{v.name}{health}{equip}: '
                f'{ranged}'
                f'{int(round(v.average_damage(copy(context), front_size, nb) * 10))}'
                f'/{int(round(v.average_health(context, nb)))} '
                f'{v.describe_formation(context, front_size, nb)} '
                f'M{v.speed_grade(context)}{flight}')
