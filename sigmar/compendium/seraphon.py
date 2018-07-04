from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import SELF_NUMBERS
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import ignore_1_rend
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import add_mw_on_6_towound_in_charge
from sigmar.compendium.generic_keywords import CELESTIAL, ORDER, DAEMON

SERAPHON = 'SERAPHON'
SAURUS = 'SAURUS'


def ordered_cohort(u: Unit):
    def buff(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 20:
            return 1, 0
        return 0, 0
    for w in u.weapons:
        w.tohit.extra_bonuses.append(buff)

    def attack(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 30:
            return 1, 0
        return 0, 0
    for w in u.weapons:
        if 'Celestite' in w.name:
            w.attacks.extra_bonuses.append(attack)


saurus_warriors = Warscroll(
    'Saurus warriors', [
        [Weapon('Celestite Club', 1, 1, 4, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Spear', 2, 1, 4, 4, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 5, 10, 1, 10, 25, [
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Ordered Cohort', ordered_cohort),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, 'SAURUS WARRIORS'])


saurus_knights = Warscroll(
    'Saurus knights', [
        [Weapon('Celestite Blade', 1, 1, 3, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One\'s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
        [Weapon('Celestite Lance', 2, 1, 4, 3, 0, 1, [Rule('Blazing Lances', add_mw_on_6_towound_in_charge)]),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One\'s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
    ], 7, 5, 10, 2, 5, 25, [
        Rule('Stardrake Shield', ignore_1_rend),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, 'SAURUS KNIGHT'])
