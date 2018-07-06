from sigmar.basics.base import infantry
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import CHARGING, ENEMY_BASE, ENEMY_NUMBERS, SELF_WOUNDS, REND
from sigmar.compendium.seraphon import SERAPHONS, seraphons_by_name

warscrolls = SERAPHONS
context = {
    CHARGING: False,
    ENEMY_BASE: infantry,
    ENEMY_NUMBERS: 10,
    REND: -1,
}

test_armour = Roll(4)

# for ws in warscrolls:
#     for w_c_n, w_c_s in ws.stats(test_armour, context, nb=5).items():
#         damage, health = w_c_s
#         print(f'{ws.name} with {w_c_n}: {round(damage, 2)} dpt / {round(health, 2)} hp')

for ws in warscrolls:
    ws.simplest_stats(test_armour, context, _range=0.1, front_size=145)

# carn = seraphons_by_name['Saurus Oldblood on Carnosaur']
# for u in carn.units.values():
#     for i in range(1, u.wounds + 1):
#         carn.simplest_stats(test_armour, {SELF_WOUNDS: i})
