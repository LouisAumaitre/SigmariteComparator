from sigmar.basics.base import cavalry, infantry, large_infantry, monster
from sigmar.basics.roll import Roll
from sigmar.basics.value import DiceValue, RandomMultValue, value
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.string_constants import SELF_NUMBERS, MW_ON_WOUND_CRIT, EXTRA_WOUND_ON_CRIT, \
    EXTRA_DAMAGE_ON_CRIT_WOUND, ENEMY_KEYWORDS
from sigmar.basics.unit import Unit, WeaponRule
from sigmar.basics.unit_rules import ignore_1_rend, fly, ignore_2_rend, march_double
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import add_mw_on_6_towound_in_charge, d3_hits_on_crit
from sigmar.compendium.generic_keywords import CELESTIAL, ORDER, DAEMON, WIZARD, HERO, MONSTER, CHAOS

SERAPHONS = []

SERAPHON = 'SERAPHON'
SLAAN = 'SLAAN'
SAURUS = 'SAURUS'
SKINK = 'SKINK'
CARNOSAUR = 'CARNOSAUR'


def ordered_cohort(u: Unit):
    def buff(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 20:
            return 1, 0
        return 0, 0
    for w in u.weapons:
        w.tohit.extra_bonuses.append(buff)

    def attack(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 30:
            return 1
        return 0
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
        if w.range.average({}) > 3:
            w.tohit.extra_bonuses.append(buff)


SERAPHONS.append(Warscroll(
    'Slann Starmaster', [
        [Weapon('Azure Lightning', 3, 6, 4, 3, 1, 1, [])],
    ], 5, 4, 10, 7, 1, large_infantry, rules=[
        Rule('Fly', fly),
        Rule('Celestial Configuration', lambda x: None),
        Rule('Arcane Vassal', lambda x: None),
        Spell('Light of the Heavens', 6, None),
        CommandAbility('Gift from the Heavens', None),
    ], keywords=[ORDER, CELESTIAL, SERAPHON, SLAAN, WIZARD, HERO],
    cast=3, unbind=3))


def dead_for_innumerable_ages(u: Unit):
    u.wounds = u.bravery - DiceValue('D6').average({})


SERAPHONS.append(Warscroll(
    'Lord Kroak', [
        [Weapon('Spectral Claws', 3, "2D6", 3, 3, 1, 1, [])],
    ], 5, 4, 10, 0, 1, large_infantry, rules=[
        Rule('Fly', fly),
        Rule('Dead for Innumerable Ages', dead_for_innumerable_ages),
        Spell('Celestial Deliverance', 7, None),
        Spell('Comet`s Call', 7, None),
        CommandAbility('Impeccable Foresight', None),
    ], keywords=[ORDER, CELESTIAL, SERAPHON, SLAAN, WIZARD, HERO],
    cast=4, unbind=4, named=True))


SERAPHONS.append(Warscroll(
    'Saurus Oldblood', [
        [Weapon('Suntooth Maul', 1, 2, 3, 4, -1, 'D3', []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Warblade', 1, 4, 3, 3, 0, 1, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite War-spear', 2, 4, 4, 3, -1, 1, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Greatblade', 1, 2, 4, 3, -1, 2, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 4, 10, 7, 1, infantry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Wrath of the Seraphon', lambda x: None),
        CommandAbility('Paragon of Order', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Sunblood', [
        [Weapon('Celestite War-mace', 1, 5, 3, 3, -1, 1, []),
         Weapon('Fearsome Jaws and Aeon Shield', 1, 2, 4, 3, 0, 1, [])],
    ], 5, 4, 10, 7, 1, infantry, rules=[
        Rule('Aeon Shield', ignore_2_rend),
        WeaponRule('Ferocious Rage', d3_hits_on_crit),
        CommandAbility('Scent of Weakness', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Oldblood on Carnosaur', [
        [Weapon('Sunbolt Gauntlet', 18, 'D6', 3, 4, -1, 1, []),
         Weapon('Sunstone Spear', 2, 3, 3, 3, -1, 'D3', []),
         Weapon('Carnosaur`s Clawed Forelimbs', 2, 2, {10: 3, 5: 4, 0: 5}, 3, 0, 2, []),
         Weapon('Carnosaur`s Massive Jaws', 2, {10: 5, 8: 4, 5: 3, 3: 2, 0: 1}, 4, 3, -1, 3, [])],
    ], {8: 10, 3: 8, 0: 6}, 4, 10, 12, 1, monster, rules=[
        WeaponRule('Pinned Down', lambda x: None),
        Rule('Blood Frenzy', lambda x: None),
        Rule('Bloodroar', lambda x: None),
        WeaponRule('Blazing Sunbolts', lambda x: None),
        CommandAbility('Ancient Warlord', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO, MONSTER, CARNOSAUR, 'SAURUS OLBLOOD']))


SERAPHONS.append(Warscroll(
    'Saurus Eternity Warden', [
        [Weapon('Star-stone Mace', 1, 3, 3, 3, -1, 2, []),
         Weapon('Fearsome Jaws', 1, 1, 4, 4, 0, 1, [])],
    ], 5, 4, 10, 7, 1, infantry, rules=[
        Rule('Selfless Protector', lambda x: None),
        Rule('Alpha Warden', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Guard', [
        [Weapon('Celestite Polearm', 1, 2, 3, 3, -1, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 4, 10, 1, 5, infantry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Sworn Guardians', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS]))


SERAPHONS.append(Warscroll(
    'Saurus Scar-veteran on Carnosaur', [
        [Weapon('Celestite Warblade', 1, 6, 3, 3, 0, 1, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 4, 3, 0, 1, []),
         Weapon('Carnosaur`s Clawed Forelimbs', 2, 2, {10: 3, 5: 4, 0: 5}, 3, 0, 2, []),
         Weapon('Carnosaur`s Massive Jaws', 2, {10: 5, 8: 4, 5: 3, 3: 2, 0: 1}, 4, 3, -1, 3, [])],
        [Weapon('Celestite War-spear', 2, 6, 4, 3, -1, 1, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 4, 3, 0, 1, []),
         Weapon('Carnosaur`s Clawed Forelimbs', 2, 2, {10: 3, 5: 4, 0: 5}, 3, 0, 2, []),
         Weapon('Carnosaur`s Massive Jaws', 2, {10: 5, 8: 4, 5: 3, 3: 2, 0: 1}, 4, 3, -1, 3, [])],
        [Weapon('Celestite Greatblade', 1, 3, 4, 3, -1, 2, []),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 4, 3, 0, 1, []),
         Weapon('Carnosaur`s Clawed Forelimbs', 2, 2, {10: 3, 5: 4, 0: 5}, 3, 0, 2, []),
         Weapon('Carnosaur`s Massive Jaws', 2, {10: 5, 8: 4, 5: 3, 3: 2, 0: 1}, 4, 3, -1, 3, [])],
    ], {8: 10, 3: 8, 0: 6}, 4, 10, 12, 1, monster, rules=[
        WeaponRule('Pinned Down', lambda x: None),
        Rule('Blood Frenzy', lambda x: None),
        Rule('Bloodroar', lambda x: None),
        Rule('Stardrake Shield', ignore_1_rend),
        CommandAbility('Saurian Savagery', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO, MONSTER, CARNOSAUR]))


def fury_of_the_seraphon(w: Weapon):
    w.attacks = RandomMultValue((1.5+1/12), 3, w.attacks)


SERAPHONS.append(Warscroll(
    'Saurus Scar-veteran on Cold-One', [
        [Weapon('Celestite War-pick', 1, 3, 3, 3, -1, 1, [Rule('Fury of the Seraphon', fury_of_the_seraphon)]),
         Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 4, 3, 0, 1, []),
         Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
    ], 10, 4, 10, 7, 1, cavalry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        CommandAbility('Savage Charge', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Warriors', [
        [Weapon('Celestite Club', 1, 1, 4, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Spear', 2, 1, 4, 4, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 5, 10, 1, 10, infantry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Ordered Cohort', ordered_cohort),
        Rule('Wardrum', march_double),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS]))


SERAPHONS.append(Warscroll(
    'Saurus Astrolith Bearer', [
        [Weapon('Celestite War-pick', 1, 3, 3, 3, -1, 1, []),
         Weapon('Fearsome Jaws', 1, 1, 4, 4, 0, 1, [])],
    ], 10, 4, 10, 7, 1, cavalry, rules=[
        Rule('Celestial Conduit', lambda x: None),
        Rule('Proud Defiance', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Knights', [
        [Weapon('Celestite Blade', 1, 1, 3, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
        [Weapon('Celestite Lance', 2, 1, 4, 3, 0, 1, [Rule('Blazing Lances', add_mw_on_6_towound_in_charge)]),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, []),
         Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])],
    ], 7, 5, 10, 2, 5, cavalry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Wardrum', march_double),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS]))

SERAPHONS.append(Warscroll(
    'Skink Starseer', [
        [Weapon('Astromancer`s Staff', 2, 1, 4, 4, -1, 'D3', [])],
    ], 8, 4, 10, 5, 1, infantry, rules=[
        Rule('Fly', fly),
        Rule('Cosmic Herald', lambda x: None),
        Spell('Curse of Fate', 4, None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK, HERO, WIZARD],
    cast=1, unbind=1))

SERAPHONS.append(Warscroll(
    'Skink Starpriest', [
        [Weapon('Star-stone Dagger', 1, 3, 3, 4, -1, 1, [])],
    ], 8, 5, 10, 4, 1, infantry, rules=[
        Rule('Serpent Staff', lambda x: None),
        Spell('Summon  Starlight', 6, None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK, HERO, WIZARD],
    cast=1, unbind=1))

SERAPHONS.append(Warscroll(
    'Troglodon', [
        [Weapon('Noxious Spittle', {10: 18, 8: 15, 5: 12, 3: 9, 0: 6}, 'D3', 3, 3, 0, 2, []),
         Weapon('Venomous Bite', 2, 6, 4, {10: 2, 5: 3, 3: 4, 0: 5}, 0, 2, []),
         Weapon('Troglodon`s Clawed Forelimbs', 2, 2, 4, 3, 0, 2, []),
         Weapon('Skink Oracle`s Divining Rod', 1, 1, 4, 5, 0, 1, [])],
    ], {10: 10, 8: 9, 5: 8, 3: 7, 0: 6}, 4, 10, 12, 1, monster, rules=[
        Rule('Divining Rod', lambda x: None),
        Rule('Primeval Roar', lambda x: None),
        Rule('Drawn to the Screams', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK, HERO, MONSTER], unbind=1))


def cloak_of_feathers(u: Unit):
    print('FEATHERS')
    fly(u)
    u.move = value(14)
    u.save = Roll(4)


SERAPHONS.append(Warscroll(
    'Skink Priest', [
        [Weapon('Starbolt', 18, 'D3', 3, 3, -1, 1, []),
         Weapon('Star-stone Staff', 1, 3, 4, 3, -1, 1, []),
         Rule('Cloak of Feathers', cloak_of_feathers)],
        [Weapon('Starbolt', 18, 'D3', 3, 3, -1, 1, []),
         Weapon('Star-stone Staff', 1, 3, 4, 3, -1, 1, []),
         Rule('Priestly Trappings', lambda x: None)],
    ], 8, 5, 10, 4, 1, infantry, rules=[
        Rule('Celestial Rites', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK, HERO]))

SERAPHONS.append(Warscroll(
    'Skinks', [
        [Weapon('Meteoritic Javelin', 8, 1, 5, 4, 0, 1, []),
         Weapon('Meteoritic Javelin', 1, 1, 6, 5, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
        [Weapon('Boltspitter', 16, 1, 5, 5, 0, 1, []),
         Weapon('Boltspitter', 1, 1, 5, 6, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
        [Weapon('Boltspitter', 16, 1, 5, 5, 0, 1, []),
         Weapon('Boltspitter', 1, 1, 5, 6, 0, 1, []),
         Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, []),
         Rule('Star-buckler', ignore_1_rend)],
    ], 8, 6, 10, 1, 10, infantry, rules=[
        Rule('Celestial cohort', celestial_cohort),
        Rule('Wary Fighters', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON]))


def star_venom(w: Weapon):
    def buff(data):
        if CHAOS in data.get(ENEMY_KEYWORDS, []) and DAEMON in data.get(ENEMY_KEYWORDS, []):
            data[EXTRA_DAMAGE_ON_CRIT_WOUND] = 2
        else:
            data[EXTRA_DAMAGE_ON_CRIT_WOUND] = 1

    w.attack_rules.append(buff)


SERAPHONS.append(Warscroll(
    'Chameleon Skinks', [
        [Weapon('Dartpipe', 16, 2, 3, 4, 0, 1, [Rule('Star-venom', star_venom)]),
         Weapon('Envenomed Dart', 1, 1, 5, 5, 0, 1, [])]
    ], 8, 6, 10, 1, 5, infantry, rules=[
        Rule('Chameleon Ambush', lambda x: None),
        Rule('Disappear from Sight', lambda x: None),
        Rule('Perfect Mimicry', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK]))


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
    ], 8, 4, 10, 4, 3, large_infantry, rules=[
        Rule('Energy transcendence', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON]))

seraphons_by_name = {unit.name: unit for unit in SERAPHONS}
