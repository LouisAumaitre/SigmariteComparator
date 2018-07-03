from sigmar.basics.random_value import rv
from sigmar.basics.rules import Rule
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import reroll_1_tohit, reroll_all_tohit
from sigmar.compendium.stormcast_eternals import liberators

units = [
    liberators
]

for u in units:
    print(f'{u.name}: {round(u.average_damage(), 2)} dpt')
