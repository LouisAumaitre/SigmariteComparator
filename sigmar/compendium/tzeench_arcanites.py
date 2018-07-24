from sigmar.basics.base import monster_base, large_infantry_base, infantry_base
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import fly
from sigmar.basics.value import value, RandomValue
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import extra_damage_on_keyword
from sigmar.compendium.generic_keywords import CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER

TZEENTCH_WS = []

HORROR = 'HORROR'


def mastery_of_magic(u: Unit):
    # when casting/unbinding a spell, the lowest dice becomes equal to the highest
    u.casting_value = RandomValue({2: 1/36, 4: 3/36, 6: 5/36, 8: 7/36, 10: 9/36, 12: 11/36})
    u.unbinding_value = RandomValue({2: 1/36, 4: 3/36, 6: 5/36, 8: 7/36, 10: 9/36, 12: 11/36})


TZEENTCH_WS.append(Warscroll(
    'Lord of Change', [
        [Weapon('Rod of Sorcery', 18, '2D6', 3, 3, 0, 1, []),
         Weapon('Staff of Tzeentch', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
        [Weapon('Staff of Tzeentch', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Baleful Sword', 1, 2, 4, 2, -2, 3, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', mastery_of_magic),
        Rule('Spell-thief', lambda x: None),
        CommandAbility('Beacon of Sorcery', None),
        Spell('Infernal Gateway', 7, None),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER], cast=2, unbind=2))


TZEENTCH_WS.append(Warscroll(
    'Kairos Fateweaver', [
        [Weapon('Staff of Tomorrow', 3, 2, 4, {11: 2, 5: 3, 0: 4}, -1, 2, []),
         Weapon('Beaks and Talons', 1, 5, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', mastery_of_magic),
        Rule('Oracle of Eternity', lambda x: None),
        Spell('Gift of Change', 8, None),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER, 'LORD OF CHANGE'], cast=2, unbind=2, named=True))


TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch on Burning Chariot', [
        [Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [
             Rule('Sky-sharks', extra_damage_on_keyword(value('D3') - 1, MONSTER))
         ])],
        [Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [
             Rule('Sky-sharks', extra_damage_on_keyword(value('D3') - 1, MONSTER))
         ])],
    ], 14, 5, 10, 8, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Arcane Tome', lambda x: None),
        Rule('Wake of Fire', lambda x: None),
        Spell('Tzeentch`s Firestorm', 9, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))


TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch on Disc', [
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
    ], 16, 5, 10, 5, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
        Rule('Arcane Tome', lambda x: None),
        Spell('Blue Fire of Tzeentch', 4, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))


TZEENTCH_WS.append(Warscroll(
    'The Changeling', [
        [Weapon('The Trickster`s Staff', 2, 1, 4, 3, -1, 'D3', [])],
    ], 5, 5, 10, 5, 1, infantry_base, rules=[
        Rule('Arch-Deceiver', lambda x: None),
        Rule('Puckish Misdirection', lambda x: None),
        Rule('Formless Horror', lambda x: None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1, named=True))


def fortune_and_fate(u: Unit):
    # when casting a spell, any roll of 9 or more gives an extra spell
    potential_cast = u.casting_value.potential_values({})
    one = sum([proba for cast, proba in potential_cast if cast < 9])
    two = sum([proba for cast, proba in potential_cast if cast >= 9])
    three = two * two
    u.spells_per_turn = RandomValue({
        1: one,
        2: two - three,
        3: three
    })


TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch', [
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', [])],
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, [])],
    ], 5, 5, 10, 5, 1, infantry_base, rules=[
        Rule('Arcane Tome', lambda x: None),
        Rule('Fortune and Fate', fortune_and_fate),
        Spell('Pink Fire of Tzeentch', 9, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))

tzeentchites_by_name = {unit.name: unit for unit in TZEENTCH_WS}
