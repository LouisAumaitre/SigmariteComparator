from typing import Union, List, Dict, Tuple, Any

from copy import copy

from sigmar.basics.base import Base
from sigmar.basics.value import Value, value
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule, CommandAbility, Spell, MAGIC_SHIELD, ARCANE_BOLT
from sigmar.basics.string_constants import SELF_NUMBERS, SELF_BASE, INCH, SELF_WOUNDS, REND, RANGE, SELF_MOVE
from sigmar.basics.weapon import Weapon
from sigmar.compendium.generic_keywords import MONSTER, HERO


class Unit:
    def __init__(
            self,
            name: str,
            weapons: Union[List[Weapon]],
            move: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            save: int,
            bravery: int,
            wounds: int,
            min_size: int,
            base: Base,
            rules: List[Rule],
            keywords: List[str],
            cast=0,
            unbind=0,
            named=False,
            max_size=None,
    ):
        self.name = name
        self.weapons = weapons
        self.move = value(move)
        self.save = Roll(save)
        self.extra_save = Roll(7)
        self.bravery = bravery
        self.wounds = wounds
        self.min_size = min_size
        self.size = min_size
        self.max_size = max_size
        if self.max_size is None:
            self.max_size = min_size if 'MONSTER' in keywords or 'HERO' in keywords else min_size
        self.base = base
        self.keywords = keywords
        keywords.append(self.name.upper())
        self.named = named
        self.can_fly = False
        self.run_distance = value('D6')
        self.charge_range = value('2D6')
        self.can_run_and_charge = False
        self.special_users = []
        self.casting_value = value('2D6')
        self.unbinding_value = value('2D6')
        self.morale_roll = value('D6')
        self.notes = []

        self.spells_per_turn = value(cast)
        self.unbind_per_turn = value(unbind)
        self.spells: List[Spell] = [ARCANE_BOLT, MAGIC_SHIELD]
        self.command_abilities: List[CommandAbility] = []

        self.rules = rules
        for r in self.rules:
            r.apply(self)

    def formation(self, data: dict, front_size) -> List[int]:
        nb = data.get(SELF_NUMBERS, self.size)
        data[SELF_NUMBERS] = nb
        rows = []
        while nb > 0:
            row = max(min(front_size // self.base.width, nb), 1)
            rows.append(row)
            nb -= row
        return rows

    def describe_formation(self, data: dict, front_size) -> str:
        rows = self.formation(data, front_size)
        if len(rows) == 1 and rows[0] <= 1:
            return ''
        attacking = 0
        _range = data.get(RANGE, 0)
        for row in rows:
            if sum([1 if w.range.average(data) > _range else 0 for w in self.weapons if isinstance(w, Weapon)]):
                attacking += row
            else:
                break
            _range += self.base.depth / INCH
        if len(rows) > 1:
            return f'({rows[0]}x{len(rows)}, {attacking} attacking)'
        return f'({attacking} attacking)'

    def average_damage(self, data: dict, front_size=1000):
        total = 0
        unit_data = copy(data)
        unit_data[SELF_BASE] = self.base
        unit_data[SELF_MOVE] = self.move.average(data)
        _range = data.get(RANGE, 0)
        data[RANGE] = _range
        for row in self.formation(unit_data, front_size):
            # specials
            specials = 0
            if total == 0:
                for sp_usr in self.special_users:
                    total += sp_usr.size * sum([w.average_damage(copy(unit_data)) for w in sp_usr.weapons])
                    specials += sp_usr.size

            users = row - specials
            if users <= 5:
                total += sum([w.average_damage(copy(unit_data), users=users) for w in self.weapons])
            else:  # let's avoid taking years to compute
                total += users * sum([w.average_damage(copy(unit_data)) for w in self.weapons])
            data[RANGE] += self.base.depth / INCH
        data[RANGE] = _range
        return total

    def average_health(self, context: dict):
        nb = context.get(SELF_NUMBERS, self.size)
        rend = context.get(REND, 0)
        save, crit = self.save.chances(context, mod=rend)
        save += crit
        wounds = min(self.wounds, context.get(SELF_WOUNDS, self.wounds))
        life = nb * wounds / (1 - save)
        life /= self.extra_save.fail(context)
        return life

    def average_speed(self, context: dict):
        average_move = self.move.average(context)
        average_sprint = self.run_distance.average(context) + average_move
        average_charge = self.charge_range.average(context) + average_move
        if self.can_run_and_charge:
            average_charge += self.run_distance.average(context)
        return average_move, average_sprint, average_charge

    def speed_grade(self, context: dict):
        m, s, c = self.average_speed(context)
        return round((m + s + c) / 3) - 3

    def speed_description(self, context: dict):
        flight = 'F' if self.can_fly else ''
        m, s, c = self.average_speed(context)
        return f'{int(round(m))}-{int(round(s))}-{int(round(c))}{flight}'

    def magic_power(self, context: dict):
        if self.spells_per_turn == 0:
            return 0
        potential_cast = self.casting_value.potential_values(context)
        spells = []
        for sp in self.spells:
            chances = sum(proba for val, proba in potential_cast if val >= sp.power)
            spells.append(chances * sp.power)
        return self.spells_per_turn.average(context) * sum(spells) / len(spells)

    def unbind_power(self, context: dict):
        if self.unbind_per_turn == 0:
            return 0
        potential_unbind = self.unbinding_value.potential_values(context)
        spells = []
        for sp_power in [5, 6, 7, 8, 9]:
            chances = sum(proba for val, proba in potential_unbind if val >= sp_power)
            spells.append(chances * sp_power)
        return self.unbind_per_turn.average(context) * sum(spells) / len(spells)

    def morale_grade(self, context: dict):
        if HERO in self.keywords or MONSTER in self.keywords:
            return self.bravery
        mod = value('D6').average(context) - self.morale_roll.average(context)
        return self.bravery + mod


class WeaponRule(Rule):
    def apply(self, item):
        if isinstance(item, Weapon):
            self.effect(item)
        elif isinstance(item, Unit):
            self.apply(item.weapons)
        elif isinstance(item, list):
            for i in item:
                self.apply(i)


class SpecialUser(Unit):
    def __init__(
            self,
            parent_args: Tuple[Any, ...],
            parent_rules,
            parent_kwargs: dict,
            name,
            weapons,
            rules,
            max_amount,
            **kwargs):  # TODO: improve def
        defaults = {
            'move': parent_args[0],
            'save': parent_args[1],
            'bravery': parent_args[2],
            'wounds': parent_args[3],
            'min_size': 1,
            'base': parent_args[5],
            'rules': [*parent_rules, *rules],
            'keywords': parent_kwargs['keywords'],
        }
        for k, v in kwargs.items():
            defaults[k] = v
        Unit.__init__(self, name, weapons, **defaults)
        self.max_amount = max_amount
