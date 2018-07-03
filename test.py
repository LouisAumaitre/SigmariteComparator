from sigmar.basics.random_value import rv
from sigmar.basics.rules import Rule
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import reroll_1_tohit, reroll_all_tohit

weapons = [
    Weapon('Sigmarite Sword', rv(1), 3, 4, 0, rv(1), []),
    Weapon('Sigmarite Hammer', rv(1), 4, 3, 0, rv(1), []),
    Weapon('Sigmarite Swords', rv(1), 3, 4, 0, rv(1), [Rule('Paired', reroll_1_tohit)]),
    Weapon('Sigmarite Hammers', rv(1), 4, 3, 0, rv(1), [Rule('Paired', reroll_1_tohit)]),
    Weapon('Sigmarite Swords ++', rv(1), 3, 4, 0, rv(1), [Rule('Paired', reroll_all_tohit)]),
    Weapon('Sigmarite Hammers ++', rv(1), 4, 3, 0, rv(1), [Rule('Paired', reroll_all_tohit)]),
]

for w in weapons:
    print(f'{w.name}: {round(w.average_damage(), 2)} dpt')
