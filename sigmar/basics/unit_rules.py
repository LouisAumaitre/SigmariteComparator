from sigmar.basics.unit import Unit


def fly(u: Unit):
    u


def reroll_1_save(u: Unit):
    u.save.rerolls = 1


def ignore_1_rend(u: Unit):
    u.ignores_1_rend = True
