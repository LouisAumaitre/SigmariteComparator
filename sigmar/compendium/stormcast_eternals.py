from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import reroll_1_save
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import reroll_1_tohit

sigmarite_shields = Rule('Sigmarite shields', reroll_1_save)

liberators = Unit(
    'Liberators', [
        [Weapon('Warhammer', 2, 4, 3, 0, 1, []), sigmarite_shields],
        [Weapon('Warblade', 2, 3, 4, 0, 1, []), sigmarite_shields],
        [Weapon('Warhammer', 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Warblade', 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Grandhammer', 2, 4, 3, 1, 2, []), sigmarite_shields],
        [Weapon('Grandblade', 2, 4, 3, 1, 2, []), sigmarite_shields],
        [Weapon('Grandhammer', 2, 4, 3, 1, 2, [])],
        [Weapon('Grandblade', 2, 4, 3, 1, 2, [])],
    ], 5, 4, 6, 2, [])
