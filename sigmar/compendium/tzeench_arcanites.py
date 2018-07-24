from sigmar.basics.base import monster_base
from sigmar.basics.rules import Rule, Spell, CommandAbility
from sigmar.basics.unit_rules import fly
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
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

tzeenchites_by_name = {unit.name: unit for unit in TZEENCH_WS}
