from sigmar.basics.base import cavalry, infantry, large_infantry
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.string_constants import SELF_NUMBERS, MW_ON_WOUND_CRIT, EXTRA_WOUND_ON_CRIT
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import ignore_1_rend, fly
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import add_mw_on_6_towound_in_charge
from sigmar.compendium.generic_keywords import CELESTIAL, ORDER, DAEMON, WIZARD, HERO


SERAPHONS = []

SERAPHON = 'SERAPHON'
SLAAN = 'SLAAN'
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


def celestial_cohort(u: Unit):
    def buff(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 30:
            return 2, 0
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 20:
            return 1, 0
        return 0, 0
    for w in u.weapons:
        if w.range > 3:
            w.tohit.extra_bonuses.append(buff)


SERAPHONS.append(Warscroll(
    'Slann Starmaster', [
        [Weapon('Azure Lightning', 3, 6, 4, 3, 1, 1, [])],
    ], 5, 4, 10, 7, 1, large_infantry, [
        Rule('Fly', fly),
        Rule('Celestial Configuration', lambda x: None),
        Rule('Arcane Vassal', lambda x: None),
        Spell('Light of the Heavens', 6, None),
        CommandAbility('Gift from the Heavens', None),
    ], [ORDER, CELESTIAL, SERAPHON, SLAAN, WIZARD, HERO, 'SLAAN STARMASTER'],
    cast=3, unbind=3))


SERAPHONS.append(Warscroll(
    'Saurus Warriors', [
        [Weapon('Celestite Club', 1, 1, 4, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Spear', 2, 1, 4, 4, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 5, 10, 1, 10, infantry, [
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Ordered Cohort', ordered_cohort),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, 'SAURUS WARRIORS']))


SERAPHONS.append(Warscroll(
    'Saurus Knights', [
        [Weapon('Celestite Blade', 1, 1, 3, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
        [Weapon('Celestite Lance', 2, 1, 4, 3, 0, 1, [Rule('Blazing Lances', add_mw_on_6_towound_in_charge)]),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
    ], 7, 5, 10, 2, 5, cavalry, [
        Rule('Stardrake Shield', ignore_1_rend),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, 'SAURUS KNIGHT']))


SERAPHONS.append(Warscroll(
    'Skinks', [
        [Weapon('Meteoritic Javelin', 8, 1, 5, 4, 0, 1, []),
         Weapon('Meteoritic Javelin', 1, 1, 6, 5, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
        [Weapon('Boltsplitter', 16, 1, 5, 5, 0, 1, []),
         Weapon('Boltsplitter', 1, 1, 5, 6, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
        [Weapon('Boltsplitter', 16, 1, 5, 5, 0, 1, []),
         Weapon('Boltsplitter', 1, 1, 5, 6, 0, 1, []),
         Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
    ], 8, 6, 10, 1, 10, infantry, [
        Rule('Celestial cohort', celestial_cohort),
        Rule('Wary Fighters', lambda x: None),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, 'SKINKS']))


def steel_trap_jaws(w: Weapon):
    def buff(data):
        data[MW_ON_WOUND_CRIT] = 35/36
        data[EXTRA_WOUND_ON_CRIT] = -15/36
    w.attack_rules.append(buff)


SERAPHONS.append(Warscroll(
    'Kroxigors', [
        [Weapon('Drakebite Maul', 2, 4, 4, 3, 0, 2, []),
         Weapon('Vice-like Jaws', 1, 1, 4, 3, 1, 1, [Rule('Jaws like a steel trap', steel_trap_jaws)])],
        [Weapon('Moon-hammer', 2, 'all_in_range', 4, 3, 1, 2, []),
         Weapon('Vice-like Jaws', 1, 1, 4, 3, 1, 1, [Rule('Jaws like a steel trap', steel_trap_jaws)])],
    ], 8, 4, 10, 4, 3, large_infantry, [
        Rule('Energy transcendence', lambda x: None),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, 'KROXIGORS']))

seraphons_by_name = {unit.name: unit for unit in SERAPHONS}
