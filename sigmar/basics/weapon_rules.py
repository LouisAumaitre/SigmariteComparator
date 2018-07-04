from sigmar.basics.string_constants import WOUNDS
from sigmar.basics.weapon import Weapon


def reroll_1_tohit(w: Weapon):
    w.tohit.rerolls = 1


def reroll_all_tohit(w: Weapon):
    w.tohit.rerolls = 5


def plus_1_tohit_5_wounds(w: Weapon):
    def buff(data):
        if WOUNDS in data and data[WOUNDS] >= 5:
            return 1, 0
        return 0, 0
    w.tohit.extra_bonuses.append(buff)
