from typing import Union

from sigmar.basics.string_constants import (
    ENEMY_WOUNDS, CHARGING, MW_ON_WOUND_CRIT, EXTRA_HIT_ON_CRIT,
    AUTO_WOUND_ON_CRIT,
    EXTRA_ATTACK_ON_HIT, MW_IF_DAMAGE, EXTRA_DAMAGE_ON_CRIT_WOUND, CRIT_BONUS_REND,
    NUMBER_OF_HITS)
from sigmar.basics.value import value, RandomValue, Value
from sigmar.basics.weapon import Weapon


# generic rules (call in the Rule declaration)
# ex: Rule('Test', hits_on_crit('D3'))
def hits_on_crit(amount: Union[int, str, Value]):
    def rule_func(w: Weapon):
        def buff(data):
            data[EXTRA_HIT_ON_CRIT] = value(amount) - 1
        w.attack_rules.append(buff)
    return rule_func


def plus_x_tohit_y_wounds(hit_bonus: int, min_wounds: int):
    def rule_func(w: Weapon):
        def buff(data):
            if data.get(ENEMY_WOUNDS, 0) >= min_wounds:
                return hit_bonus, 0
            return 0, 0
        w.tohit.rules.append(buff)

    return rule_func


def extra_attacks_in_charge(extra_attacks: Union[int, str, Value]):
    def rule_func(w: Weapon):
        def buff(data):
            if data.get(CHARGING, False):
                return value(extra_attacks)
            return 0
        w.attacks.rules.append(buff)
    return rule_func


def multiple_hits(hits: Union[int, str, Value]):
    def rule_func(w: Weapon):
        def buff(data):
            data[NUMBER_OF_HITS] = value(hits)
        w.attack_rules.append(buff)
    return rule_func


# specific rules (use as value in the Rule declaration)
# ex: Rule('Test', reroll_1_tohit)
def reroll_1_tohit(w: Weapon):
    w.tohit.rerolls = 1


def reroll_all_tohit(w: Weapon):
    w.tohit.rerolls = 5


def add_mw_on_6_towound_in_charge(w: Weapon):
    def buff(data):
        if data.get(CHARGING, False):
            data[MW_ON_WOUND_CRIT] = 1
    w.attack_rules.append(buff)


def plus_1_towound_in_charge(w: Weapon):
    def buff(data):
        if data.get(CHARGING, False):
            return 1, 0
        return 0, 0
    w.towound.rules.append(buff)


def extra_hit_on_crit(w: Weapon):
    def buff(data):
        data[EXTRA_HIT_ON_CRIT] = 1
    w.attack_rules.append(buff)


def d3_mw_on_4_if_wounded(w: Weapon):
    def hellfire(data):
        data[MW_IF_DAMAGE] = value('D3') * RandomValue({1: 0.5, 0: 0.5})
    w.attack_rules.append(hellfire)


def auto_wound_on_crit_hit(w: Weapon):
    def buff(data):
        data[AUTO_WOUND_ON_CRIT] = True
    w.attack_rules.append(buff)


def extra_attack_on_hit(w: Weapon):
    def buff(data):
        data[EXTRA_ATTACK_ON_HIT] = 1
    w.attack_rules.append(buff)


def d6_dmg_on_crit(w: Weapon):
    def buff(data):
        data[EXTRA_DAMAGE_ON_CRIT_WOUND] = value('D6') - 1
    w.attack_rules.append(buff)


def extra_3_rend_on_crit_hit(w: Weapon):
    def buff(data):
        data[CRIT_BONUS_REND] = -3
    w.attack_rules.append(buff)
