from sigmar.basics.unit import Unit
from sigmar.basics.value import value


def fly(u: Unit):
    u.can_fly = True


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
