from sigmar.basics.base import monster_base
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.unit_rules import fly
from sigmar.basics.value import value
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import extra_damage_on_keyword
from sigmar.compendium.generic_keywords import CHAOS, DAEMON, TZEENCH, WIZARD, HERO, MONSTER

TZEENCH_WS = []


TZEENCH_WS.append(Warscroll(
    'Lord of Change', [
        [Weapon('Rod of Sorcery', 18, '2D6', 3, 3, 0, 1, []),
         Weapon('Staff of Tzeench', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
        [Weapon('Staff of Tzeench', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Baleful Sword', 1, 2, 4, 2, -2, 3, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', lambda x: None),
        Rule('Spell-thief', lambda x: None),
        CommandAbility('Beacon of Sorcery', None),
        Spell('Infernal Gateway', 7, None),
    ], keywords=[CHAOS, DAEMON, TZEENCH, WIZARD, HERO, MONSTER], cast=2, unbind=2))


TZEENCH_WS.append(Warscroll(
    'Kairos Fateweaver', [
        [Weapon('Staff of Tomorrow', 3, 2, 4, {11: 2, 5: 3, 0: 4}, -1, 2, []),
         Weapon('Beaks and Talons', 1, 5, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', lambda x: None),
        Rule('Oracle of Eternity', lambda x: None),
        Spell('Gift of Change', 8, None),
    ], keywords=[CHAOS, DAEMON, TZEENCH, WIZARD, HERO, MONSTER, 'LORD OF CHANGE'], cast=2, unbind=2, named=True))


TZEENCH_WS.append(Warscroll(
    'Herald of Tzeench on Burning Chariot', [
        [Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [
             Rule('Sky-sharks', extra_damage_on_keyword(value('D3') - 1, MONSTER))
         ])],
    ], 14, 5, 10, 8, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Arcane Tome', lambda x: None),
        Rule('Wake of Fire', lambda x: None),
        Spell('Tzeench`s Firestorm', 9, None),
    ], keywords=[CHAOS, DAEMON, TZEENCH, WIZARD, HERO, MONSTER, 'LORD OF CHANGE'], cast=1, unbind=1))

tzeenchites_by_name = {unit.name: unit for unit in TZEENCH_WS}
