from typing import Union

from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.value import value, Value


def can_reroll_x_dice_during_game(amount: Union[Value, int, str]=1):
    def rule_func(u: Unit):
        u.notes.append(f'Reroll{value(amount)}')
    return rule_func


def extra_save(roll: int):
    def rule_func(u: Unit):
        u.extra_save = Roll(roll)
    return rule_func


def regeneration(amount: Union[Value, int, str]=1):
    def rule_func(u: Unit):
        u.notes.append(f'Regeneration{value(amount)}')
    return rule_func


def can_steal_spells(
        range_: Union[Value, int, str]=18,
        chances: Union[Value, int, str]=1,
        tries_per_turn: Union[Value, int, str]=1
):
    def rule_func(u: Unit):
        value(range_)
        u.notes.append(f'Spell stealer ({round(value(chances).average({}) * value(tries_per_turn).average({}), 1)})')
    return rule_func


def copy_spells(
        range_: Union[Value, int, str]=18,
):
    def rule_func(u: Unit):
        value(range_)
        pass
    return rule_func


def fly(u: Unit):
    u.can_fly = True


FLIGHT = Rule('Fly', fly)


def reroll_1_save(u: Unit):
    u.save.rerolls = 1


def ignore_1_rend(u: Unit):
    u.save.mod_ignored.append(-1)


def ignore_2_rend(u: Unit):
    u.save.mod_ignored.append(-1)
    u.save.mod_ignored.append(-2)


def march_double(u: Unit):
    u.run_distance = u.move


def charge_at_3d6(u: Unit):
    u.charge_range = value('3D6')


def run_and_charge(u: Unit):
    u.can_run_and_charge = True
