import time

from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import (
    CHARGING, ENEMY_BASE, ENEMY_NUMBERS, REND, ENEMY_KEYWORDS, RANGE,
    ENEMY_SAVE, ENEMY_WOUNDS,
    SELF_NUMBERS, DID_MOVE, SELF_MOVE, ENEMY_BRAVERY)
from sigmar.basics.warscroll import formatted_scrolls
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import deal_x_mortal_wound_on_roll
from sigmar.compendium.generic_keywords import DAEMON, CHAOS, WIZARD
from sigmar.compendium.tzeench_arcanites import TZEENTCH_WS

warscrolls = TZEENTCH_WS

test_armour = Roll(4)
context = {
    CHARGING: True,
    ENEMY_BASE: infantry_base,
    ENEMY_NUMBERS: 10,
    ENEMY_WOUNDS: 1,
    ENEMY_BRAVERY: 7,
    # DID_MOVE: False,
    ENEMY_KEYWORDS: [],
    RANGE: 0.1,
    ENEMY_SAVE: test_armour,
}

start = time.time()
formatted_scrolls(warscrolls, context, front_size=145, max_variants=3)
print(f't={time.time() - start}s')

# for k, u in seraphons_by_name['Kroxigors'].units.items():
#     for w in u.weapons:
#         print(f'{w.name}: {w.average_damage(context)}')
#     break


# w = Weapon('Wake of Fire', 3, 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll('D3', Roll(4)))])
# print(w.average_damage(context))
# print(stormcasts_by_name['Prosecutors'].units['Celestial Hammers'].speed_description(context))
# print(stormcasts_by_name['Prosecutors'].units['Celestial Hammers'].charge_range)
