from sigmar.basics.weapon import Weapon


def reroll_1_tohit(w: Weapon):
    w.reroll_tohit = 1


def reroll_all_tohit(w: Weapon):
    w.reroll_tohit = 5
