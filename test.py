import time

from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import (
    CHARGING, ENEMY_BASE, ENEMY_NUMBERS, REND, ENEMY_KEYWORDS, RANGE,
    ENEMY_SAVE, ENEMY_WOUNDS,
    SELF_NUMBERS)
from sigmar.compendium.generic_keywords import DAEMON, CHAOS
from sigmar.compendium.stormcast_eternals import STORMCAST_WS

warscrolls = STORMCAST_WS

test_armour = Roll(4)
context = {
    CHARGING: False,
    ENEMY_BASE: infantry_base,
    ENEMY_NUMBERS: 10,
    ENEMY_WOUNDS: 1,
    REND: -1,
    ENEMY_KEYWORDS: [CHAOS],
    RANGE: 0.1,
    ENEMY_SAVE: test_armour,
}

start = time.time()
for ws in warscrolls:
    ws.simplest_stats(context, front_size=145)
print(f't={time.time() - start}s')

# for k, u in warscrolls[1].units.items():
#     for w in u.weapons:
#         print(f'{w.name}: {w.average_damage(context)}')
# warscrolls[0].simplest_stats(context, front_size=145)

# w = Weapon('Stream of Fire', 8, 2, 3, 3, -2, 'D6', [Rule('It burns!', d3_mw_on_4_if_wounded)])
# print(w.average_damage(context))
