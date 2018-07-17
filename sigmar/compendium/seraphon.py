from sigmar.basics.base import cavalry, infantry, large_infantry, monster
from sigmar.basics.roll import Roll
from sigmar.basics.value import DiceValue, RandomMultValue, value
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.string_constants import (
    SELF_NUMBERS, MW_ON_WOUND_CRIT, EXTRA_WOUND_ON_CRIT,
    EXTRA_DAMAGE_ON_CRIT_WOUND, ENEMY_KEYWORDS, BONUS_REND, RANGE, EXTRA_ATTACK_ON_HIT
)
from sigmar.basics.unit import Unit, WeaponRule
from sigmar.basics.unit_rules import ignore_1_rend, fly, ignore_2_rend, march_double
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import (
    add_mw_on_6_towound_in_charge, d3_hits_on_crit, d3_mw_on_4_if_wounded,
    auto_wound_on_crit_hit, d6_hit_on_crit, reroll_all_tohit
)
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


fearsome_jaws_old_blood = Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Saurus Oldblood', [
        [Weapon('Suntooth Maul', 1, 2, 3, 4, -1, 'D3', []), fearsome_jaws_old_blood],
        [Weapon('Celestite Warblade', 1, 4, 3, 3, 0, 1, []), fearsome_jaws_old_blood],
        [Weapon('Celestite War-spear', 2, 4, 4, 3, -1, 1, []), fearsome_jaws_old_blood],
        [Weapon('Celestite Greatblade', 1, 2, 4, 3, -1, 2, []), fearsome_jaws_old_blood],
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


carnosaur_forelimbs = Weapon('Carnosaur`s Clawed Forelimbs', 2, 2, {10: 3, 5: 4, 0: 5}, 3, 0, 2, [])
carnosaur_jaws = Weapon('Carnosaur`s Massive Jaws', 2, {10: 5, 8: 4, 5: 3, 3: 2, 0: 1}, 4, 3, -1, 3, [])


SERAPHONS.append(Warscroll(
    'Saurus Oldblood on Carnosaur', [
        [Weapon('Sunbolt Gauntlet', 18, 'D6', 3, 4, -1, 1, [Rule('Blazing Sunbolts', lambda x: None)]),
         Weapon('Sunstone Spear', 2, 3, 3, 3, -1, 'D3', []),
         carnosaur_forelimbs, carnosaur_jaws],
    ], {8: 10, 3: 8, 0: 6}, 4, 10, 12, 1, monster, rules=[
        WeaponRule('Pinned Down', lambda x: None),
        Rule('Blood Frenzy', lambda x: None),
        Rule('Bloodroar', lambda x: None),
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


powerful_jaws_and_shield = Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Saurus Guard', [
        [Weapon('Celestite Polearm', 1, 2, 3, 3, -1, 1, []), powerful_jaws_and_shield],
    ], 5, 4, 10, 1, 5, infantry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Sworn Guardians', lambda x: None),
        Rule('Wardrum', march_double),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS],
    special_options=[{
        'name': 'Alpha Guardian',
        'weapons': [Weapon('Celestite Polearm', 1, 3, 3, 3, -1, 1, []), powerful_jaws_and_shield]
    }]))


fearsome_jaws_scar_veteran = Weapon('Fearsome Jaws and Stardrake Shield', 1, 1, 4, 3, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Saurus Scar-veteran on Carnosaur', [
        [Weapon('Celestite Warblade', 1, 6, 3, 3, 0, 1, []),
         fearsome_jaws_scar_veteran, carnosaur_forelimbs, carnosaur_jaws],
        [Weapon('Celestite War-spear', 2, 6, 4, 3, -1, 1, []),
         fearsome_jaws_scar_veteran, carnosaur_forelimbs, carnosaur_jaws],
        [Weapon('Celestite Greatblade', 1, 3, 4, 3, -1, 2, []),
         fearsome_jaws_scar_veteran, carnosaur_forelimbs, carnosaur_jaws],
    ], {8: 10, 3: 8, 0: 6}, 4, 10, 12, 1, monster, rules=[
        WeaponRule('Pinned Down', lambda x: None),
        Rule('Blood Frenzy', lambda x: None),
        Rule('Bloodroar', lambda x: None),
        Rule('Stardrake Shield', ignore_1_rend),
        CommandAbility('Saurian Savagery', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO, MONSTER, CARNOSAUR]))


def fury_of_the_seraphon(w: Weapon):
    w.attacks = RandomMultValue((1.5+1/12), 3, w.attacks)


cold_one_bite = Weapon('Cold One`s Vicious Bite', 1, 2, 3, 4, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Saurus Scar-veteran on Cold-One', [
        [Weapon('Celestite War-pick', 1, 3, 3, 3, -1, 1, [Rule('Fury of the Seraphon', fury_of_the_seraphon)]),
         fearsome_jaws_scar_veteran, cold_one_bite],
    ], 10, 4, 10, 7, 1, cavalry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        CommandAbility('Savage Charge', None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, HERO]))


SERAPHONS.append(Warscroll(
    'Saurus Warriors', [
        [Weapon('Celestite Club', 1, 1, 4, 3, 0, 1, []), powerful_jaws_and_shield],
        [Weapon('Celestite Spear', 2, 1, 4, 4, 0, 1, []), powerful_jaws_and_shield],
    ], 5, 5, 10, 1, 10, infantry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Ordered Cohort', ordered_cohort),
        Rule('Wardrum', march_double),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS],
    special_options=[{
        'name': 'Alpha Talon',
        'weapons': [
            Weapon('Celestite Club', 1, 2, 4, 3, 0, 1, []), powerful_jaws_and_shield],
    }, {
        'name': 'Alpha Talon',
        'weapons': [
            Weapon('Celestite Spear', 2, 2, 4, 4, 0, 1, []), powerful_jaws_and_shield],
    }]))


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
        [Weapon('Celestite Blade', 1, 1, 3, 3, 0, 1, []), powerful_jaws_and_shield, cold_one_bite],
        [Weapon('Celestite Lance', 2, 1, 4, 3, 0, 1, [Rule('Blazing Lances', add_mw_on_6_towound_in_charge)]),
         powerful_jaws_and_shield, cold_one_bite],
    ], 7, 5, 10, 2, 5, cavalry, rules=[
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Wardrum', march_double),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS],
    special_options=[{
        'name': 'Alpha Knight',
        'weapons': [Weapon('Celestite Blade', 1, 2, 3, 3, 0, 1, []), powerful_jaws_and_shield, cold_one_bite],
    }, {
        'name': 'Alpha Knight',
        'weapons': [
            Weapon('Celestite Lance', 2, 2, 4, 3, 0, 1, [Rule('Blazing Lances', add_mw_on_6_towound_in_charge)]),
            powerful_jaws_and_shield, cold_one_bite],
    }]))

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


meteoritic_javelin = Weapon('Meteoritic Javelin', 8, 1, 5, 4, 0, 1, [])
boltspitter = Weapon('Boltspitter', 16, 1, 5, 5, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Skinks', [
        [meteoritic_javelin, Weapon('Meteoritic Javelin', 1, 1, 6, 5, 0, 1, []), Rule('Star-buckler', ignore_1_rend)],
        [boltspitter, Weapon('Boltspitter', 1, 1, 5, 6, 0, 1, []), Rule('Star-buckler', ignore_1_rend)],
        [boltspitter, Weapon('Boltspitter', 1, 1, 5, 6, 0, 1, []),
         Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Moonstone Club', 1, 1, 5, 4, 0, 1, []), Rule('Star-buckler', ignore_1_rend)],
    ], 8, 6, 10, 1, 10, infantry, rules=[
        Rule('Celestial cohort', celestial_cohort),
        Rule('Wary Fighters', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON],
    special_options=[{
        'name': 'Alpha',
        'weapons': [meteoritic_javelin, Weapon('Meteoritic Javelin', 1, 2, 6, 5, 0, 1, [])],
        'rules': [Rule('Star-buckler', ignore_1_rend)],
    }, {
        'name': 'Alpha',
        'weapons': [boltspitter, Weapon('Boltspitter', 1, 2, 5, 6, 0, 1, [])],
        'rules': [Rule('Star-buckler', ignore_1_rend)],
    }, {
        'name': 'Alpha',
        'weapons': [boltspitter, Weapon('Boltspitter', 1, 2, 5, 6, 0, 1, []),
                    Weapon('Moonstone Club', 1, 2, 5, 4, 0, 1, [])],
    }, {
        'name': 'Alpha',
        'weapons': [Weapon('Moonstone Club', 1, 2, 5, 4, 0, 1, [])],
        'rules': [Rule('Star-buckler', ignore_1_rend)],
    }]))


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
         Weapon('Vice-like Jaws', 1, 1, 4, 3, -1, 1, [Rule('Jaws like a steel trap', steel_trap_jaws)])],
    ], 8, 4, 10, 4, 3, large_infantry, rules=[
        Rule('Energy transcendence', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON],
    special_options=[{'weapons': [
        Weapon('Moon-hammer', 2, 'all_in_range', 4, 3, -1, 2, []),
        Weapon('Vice-like Jaws', 1, 1, 4, 3, -1, 1, [Rule('Jaws like a steel trap', steel_trap_jaws)])
    ]}]))


SERAPHONS.append(Warscroll(
    'Salamanders', [
        [Weapon('Stream of Fire', 8, 1, 3, 3, -2, 'D6', [Rule('It burns!', d3_mw_on_4_if_wounded)]),
         Weapon('Corrosive Bite', 1, 3, 3, 3, -1, 1, [])],
    ], 8, 5, 10, 3, 1, large_infantry, rules=[
        Rule('Goaded to Fury', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON]))


def piercing_barbs(w: Weapon):
    def buff(data):
        if data[RANGE] <= 6:
            data[BONUS_REND] = data.get(BONUS_REND, 0) - 1
    w.attack_rules.append(buff)


SERAPHONS.append(Warscroll(
    'Razordons', [
        [Weapon('Volley of Spikes', 12, '2D6', 3, 4, 0, 1, [Rule('Piercing Barbs', piercing_barbs)]),
         Weapon('Fierce Bite and Spiked Tail', 1, 3, 4, 3, 0, 1, [])],
    ], 8, 4, 10, 3, 1, large_infantry, rules=[
        Rule('Goaded to Anger', lambda x: None),
        Rule('Instinctive Defense', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON]))

SERAPHONS.append(Warscroll(
    'Skink Handlers', [
        [Weapon('Goad-spears', 2, 1, 5, 5, 0, 1, [Rule('Aim for Their Eyes', auto_wound_on_crit_hit)])],
    ], 8, 6, 10, 1, 1, infantry, rules=[], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK]))


def impervious_defense(u: Unit):
    u.save.mod_ignored = [-1, -2, -3, -4, -5, -6]


SERAPHONS.append(Warscroll(
    'Bastiladon', [
        [Weapon('Searing Beam', 20, '2D6', 4, 3, -1, 2, [Rule('Light of the Heavens', lambda x: None)]),
         Weapon('Meteoritic Javelins', 8, 4, 5, 4, 0, 1, []),
         Weapon('Bludgeoning Tail', 2, 3, 3, 3, -1, 'D3', [])],
        [Weapon('Ark of Sotek', 8, 'D6', 1, 1, -6, 1, []),
         Weapon('Meteoritic Javelins', 8, 4, 5, 4, 0, 1, []),
         Weapon('Bludgeoning Tail', 2, 3, 3, 3, -1, 'D3', [])],
    ], 5, 3, 10, 8, 1, monster, rules=[
        Rule('Impervious Defense', impervious_defense),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK, MONSTER]))


terradon_beak = Weapon('Terradon`s Razor-sharp Beak', 1, 4, 4, 4, 0, 1, [])


SERAPHONS.append(Warscroll(
    'Terradon Riders', [
        [Weapon('Starstrike Javelin', 10, 2, 4, 3, 0, 1, []), terradon_beak],
        [Weapon('Sunleech Bolas', 5, 1, 4, 4, 0, 1, [Rule('Sunleech Bolas', d6_hit_on_crit)]), terradon_beak],
    ], 14, 5, 10, 3, 3, large_infantry, rules=[
        Rule('Deadly Cargo', lambda x: None),
        Rule('Swooping Dive', lambda x: None),
        Rule('Fly', fly),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK],
    special_options=[{
        'name': 'Alpha',
        'weapons': [Weapon('Starstrike Javelin', 10, 2, 3, 3, 0, 1, []), terradon_beak],
    }, {
        'name': 'Alpha',
        'weapons': [
            Weapon('Sunleech Bolas', 5, 1, 3, 4, 0, 1, [Rule('Sunleech Bolas', d6_hit_on_crit)]), terradon_beak],
    }, {
        'name': 'Skymaster',
        'weapons': [Weapon('Skyblade', 1, 3, 3, 4, 0, 1, [Rule('Skyblade', reroll_all_tohit)]), terradon_beak],
    }]))


def voracious_appetite(w: Weapon):
    def buff(data):
        data[EXTRA_ATTACK_ON_HIT] = 1
    w.attack_rules.append(buff)


SERAPHONS.append(Warscroll(
    'Ripperdactyl Riders', [
        [Weapon('Moonstone War-spear', 2, 1, 4, 4, 0, 1, []),
         Weapon('Ripperdactyl`s Slashing Claws', 1, 3, 3, 3, 0, 1, []),
         Weapon('Ripperdactyl`s Vicious Beak', 1, 1, 4, 3, 0, 1, [Rule('Voracious Appetite', voracious_appetite)])],
    ], 14, 5, 10, 3, 3, large_infantry, rules=[
        Rule('Star-buckler', ignore_1_rend),
        Rule('Swooping Dive', lambda x: None),
        Rule('Toad Rage', lambda x: None),
        Rule('Fly', fly),
    ], keywords=[ORDER, CELESTIAL, DAEMON, SERAPHON, SKINK],
    special_options=[{
        'name': 'Alpha',
        'weapons': [
            Weapon('Moonstone War-spear', 2, 2, 4, 4, 0, 1, []),
            Weapon('Ripperdactyl`s Slashing Claws', 1, 3, 3, 3, 0, 1, []),
            Weapon('Ripperdactyl`s Vicious Beak', 1, 1, 4, 3, 0, 1, [Rule('Voracious Appetite', voracious_appetite)])],
    }]))


seraphons_by_name = {unit.name: unit for unit in SERAPHONS}
