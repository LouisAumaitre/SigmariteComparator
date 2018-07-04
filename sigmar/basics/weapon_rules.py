from sigmar.basics.string_constants import WOUNDS, CHARGING
from sigmar.basics.weapon import Weapon


def reroll_1_tohit(w: Weapon):
    w.tohit.rerolls = 1


def reroll_all_tohit(w: Weapon):
    w.tohit.rerolls = 5


def plus_1_tohit_5_wounds(w: Weapon):
    def buff(data):
        if data.get(WOUNDS, 0) >= 5:
            return 1, 0
        return 0, 0
    w.tohit.extra_bonuses.append(buff)


def add_mw_on_6_towound_in_charge(w: Weapon):
    def buff(data):
        if data.get(CHARGING, False):
            return 1
        return 0
    w.towound_critical.append(buff)
