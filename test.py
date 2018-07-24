import time

from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import (
    CHARGING, ENEMY_BASE, ENEMY_NUMBERS, REND, ENEMY_KEYWORDS, RANGE,
    ENEMY_SAVE, ENEMY_WOUNDS,
    SELF_NUMBERS, DID_MOVE)
from sigmar.basics.weapon import Weapon
from sigmar.compendium.generic_keywords import DAEMON, CHAOS, WIZARD
from sigmar.compendium.tzeench_arcanites import TZEENTCH_WS

warscrolls = TZEENTCH_WS

test_armour = Roll(4)
context = {
    CHARGING: True,
    ENEMY_BASE: infantry_base,
    ENEMY_NUMBERS: 10,
    ENEMY_WOUNDS: 1,
    # DID_MOVE: False,
    REND: -1,
    ENEMY_KEYWORDS: [],
    RANGE: 0.1,
    ENEMY_SAVE: test_armour,
}

start = time.time()
for ws in warscrolls:
    ws.simplest_stats(context, front_size=145, max_variants=3)
print(f't={time.time() - start}s')

# for k, u in seraphons_by_name['Kroxigors'].units.items():
#     for w in u.weapons:
#         print(f'{w.name}: {w.average_damage(context)}')
#     break


# w = Weapon('Thunderbolt Crossbow', 18, 0, 0, 0, 0, 0, [Rule('', thunderbolt)])
# print(w.average_damage(context))
# print(stormcasts_by_name['Prosecutors'].units['Celestial Hammers'].speed_description(context))
# print(stormcasts_by_name['Prosecutors'].units['Celestial Hammers'].charge_range)
