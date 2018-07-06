from sigmar.basics.base import large_infantry
from sigmar.basics.rules import Rule
from sigmar.basics.unit import WeaponRule
from sigmar.basics.unit_rules import reroll_1_save
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import reroll_1_tohit, plus_1_tohit_5_wounds
from sigmar.compendium.generic_keywords import ORDER, HUMAN, CELESTIAL

STORMCAST_ETERNAL = 'STORMCAST ETERNAL'
REDEEMER = 'REDEEMER'

sigmarite_shields = Rule('Sigmarite shields', reroll_1_save)

liberators = Warscroll(
    'Liberators', [
        [Weapon('Warhammer', 1, 2, 4, 3, 0, 1, []), sigmarite_shields],
        [Weapon('Warblade', 1, 2, 3, 4, 0, 1, []), sigmarite_shields],
        [Weapon('Warhammers', 1, 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Warblades', 1, 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
    ], 5, 4, 6, 2, 5, large_infantry, rules=[
        WeaponRule('Lay low the Tyrants', plus_1_tohit_5_wounds),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, REDEEMER])
