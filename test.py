from sigmar.basics.roll import Roll
from sigmar.compendium.seraphon import saurus_warriors
from sigmar.compendium.stormcast_eternals import liberators

warscrolls = [
    liberators,
    saurus_warriors,
]

test_armour = Roll(4)

for ws in warscrolls:
    for w_c_n, w_c_s in ws.stats(test_armour, {}, nb=1).items():
        damage, health = w_c_s
        print(f'{ws.name} with {w_c_n}: {round(damage, 2)} dpt / {round(health, 2)} hp')

for ws in warscrolls:
    ws.simplest_stats(test_armour, {}, _range=1, front_size=180, nb=30)
