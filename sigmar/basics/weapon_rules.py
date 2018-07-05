from sigmar.basics.string_constants import ENEMY_WOUNDS, CHARGING, MW_ON_WOUND_CRIT, EXTRA_HIT_ON_CRIT
from sigmar.basics.weapon import Weapon


def reroll_1_tohit(w: Weapon):
    w.tohit.rerolls = 1


def reroll_all_tohit(w: Weapon):
    w.tohit.rerolls = 5


def plus_1_tohit_5_wounds(w: Weapon):
    def buff(data):
        if data.get(ENEMY_WOUNDS, 0) >= 5:
            return 1, 0
        return 0, 0
    w.tohit.extra_bonuses.append(buff)


def add_mw_on_6_towound_in_charge(w: Weapon):
    def buff(data):
        if data.get(CHARGING, False):
            data[MW_ON_WOUND_CRIT] = 1
    w.attack_rules.append(buff)


def extra_hit_on_crit(w: Weapon):
    def buff(data):
        data[EXTRA_HIT_ON_CRIT] = 1
    w.attack_rules.append(buff)


def d3_hits_on_crit(w: Weapon):
    def buff(data):
        data[EXTRA_HIT_ON_CRIT] = 1  # TODO: D3 - 1
    w.attack_rules.append(buff)
