from sigmar.basics.rules import Rule
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import reroll_1_save
from sigmar.basics.weapon import Weapon

liberators = Unit(
    'Liberators', [
    [Weapon('Warhammer', 1, 4, 3, 0, 1, [])]
    ], 5, 4, 6, 2, [Rule('Sigmarite shields', reroll_1_save)])
