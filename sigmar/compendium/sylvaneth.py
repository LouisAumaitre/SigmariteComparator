from sigmar.basics.base import monster
from sigmar.basics.rules import Rule, Spell
from sigmar.basics.string_constants import ENEMY_WOUNDS, MW_ON_DAMAGE
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


sylvaneth_by_name = {unit.name: unit for unit in SYLVANETH_WS}
