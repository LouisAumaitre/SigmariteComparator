from sigmar.basics.base import monster, infantry
from sigmar.basics.rules import Rule, Spell
from sigmar.basics.string_constants import ENEMY_WOUNDS, MW_ON_DAMAGE, SELF_NUMBERS
from sigmar.basics.unit import Unit
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.compendium.generic_keywords import ORDER, WIZARD, HERO, MONSTER

SYLVANETH_WS = []

SYLVANETH = 'SYLVANETH'


def impale(w: Weapon):
    def buff(data: dict):
        enemy_wounds = data.get(ENEMY_WOUNDS, 1)
        if 1 < enemy_wounds < 6:
            data[MW_ON_DAMAGE] = enemy_wounds * (6 - enemy_wounds) / 6

    w.attack_rules.append(buff)


SYLVANETH_WS.append(Warscroll(
    'Treelord Ancient', [
        [Weapon('Doom Tendril Staff', 18, 1, {10: 2, 8: 3, 5: 4, 3: 5, 0: 6}, 3, -1, 'D6', []),
         Weapon('Sweeping Blows', 3, {10: 3, 5: 2, 0: 1}, 3, 3, -1, 'D6', []),
         Weapon('Massive Impaling Talons', 1, 1, 3, {8: 2, 3: 3, 0: 4}, -2, 1, [Rule('Impale', impale)])],
    ], 5, 3, 9, 12, 1, monster, rules=[
        Rule('Groundshaking Stomp', lambda x: None),
        Rule('Spirit Path', lambda x: None),
        Spell('Awakening the Wood', 6, None),
    ], keywords=[ORDER, SYLVANETH, WIZARD, HERO, MONSTER], cast=1, unbind=1))


SYLVANETH_WS.append(Warscroll(
    'Treelord', [
        [Weapon('Strangleroots', 12, 5, {10: 2, 8: 3, 5: 4, 3: 5, 0: 6}, 3, -1, 1, []),
         Weapon('Sweeping Blows', 3, {10: 3, 5: 2, 0: 1}, 3, 3, -1, 'D6', []),
         Weapon('Massive Impaling Talons', 1, 1, 3, {8: 2, 3: 3, 0: 4}, -2, 1, [Rule('Impale', impale)])],
    ], 6, 3, 6, 12, 1, monster, rules=[
        Rule('Groundshaking Stomp', lambda x: None),
        Rule('Spirit Path', lambda x: None),
    ], keywords=[ORDER, SYLVANETH, MONSTER]))


SYLVANETH_WS.append(Warscroll(
    'Branchwraith', [
        [Weapon('Piercing Talons', 2, 3, 4, 4, -1, 1, [])],
    ], 7, 5, 8, 5, 1, infantry, rules=[
        Rule('Blessings from the Forest', lambda x: None),
        Spell('Roused to Wrath', 7, None),
    ], keywords=[ORDER, SYLVANETH, HERO, WIZARD], cast=1, unbind=1))


def impenetrable_thicket(u: Unit):
    def buff(data):
        if SELF_NUMBERS in data and data[SELF_NUMBERS] >= 12:
            return 1, 0
        return 0, 0
    u.save.extra_bonuses.append(buff)


SYLVANETH_WS.append(Warscroll(
    'Dryads', [
        [Weapon('Wracking Talons', 2, 2, 4, 4, 0, 1, [])],
    ], 7, 5, 6, 1, 5, infantry, rules=[
        Rule('Blessings from the Forest', lambda x: None),
        Rule('Enrapturing Song', lambda x: None),
        Rule('Impenetrable Thicket', impenetrable_thicket),
    ], keywords=[ORDER, SYLVANETH],
    special_options=[{
        'name': 'Branch Nymph',
        'weapons': [Weapon('Wracking Talons', 2, 3, 4, 4, 0, 1, [])]
    }]))


sylvaneth_by_name = {unit.name: unit for unit in SYLVANETH_WS}
