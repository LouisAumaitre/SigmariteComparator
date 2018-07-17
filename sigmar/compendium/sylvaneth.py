from sigmar.basics.base import monster
from sigmar.basics.rules import Rule
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.compendium.generic_keywords import ORDER, WIZARD, HERO, MONSTER

SYLVANETH_WS = []

SYLVANETH = 'SYLVANETH'


SYLVANETH_WS.append(Warscroll(
    'Treelord Ancient', [
        [Weapon('Doom Tendril Staff', 18, 1, {10: 2, 8: 3, 5: 4, 3: 5, 0: 6}, 3, -1, 'D6', []),
         Weapon('Sweeping Blows', 3, {10: 3, 5: 2, 0: 1}, 3, 3, -1, 'D6', []),
         Weapon('Massive Impaling Talons', 1, 1, 3, {8: 2, 3: 3, 0: 4}, -2, 1, [])],
    ], 5, 3, 9, 12, 1, monster, rules=[
        Rule('Blood Frenzy', lambda x: None),
        Rule('Bloodroar', lambda x: None),
    ], keywords=[ORDER, SYLVANETH, WIZARD, HERO, MONSTER]))


sylvaneth_by_name = {unit.name: unit for unit in SYLVANETH_WS}
