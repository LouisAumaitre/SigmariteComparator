from sigmar.basics.attack_round import attack_round
from sigmar.basics.base import infantry
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import (
    CHARGING, ENEMY_BASE, ENEMY_NUMBERS, REND, ENEMY_KEYWORDS, RANGE,
    ENEMY_SAVE, ENEMY_WOUNDS,
)
from sigmar.basics.value import value
from sigmar.compendium.generic_keywords import DAEMON, CHAOS
from sigmar.compendium.stormcast_eternals import STORMCAST_WS

warscrolls = STORMCAST_WS

test_armour = Roll(4)
context = {
    CHARGING: False,
    ENEMY_BASE: infantry,
    ENEMY_NUMBERS: 10,
    ENEMY_WOUNDS: 1,
    REND: -1,
    ENEMY_KEYWORDS: [CHAOS, DAEMON],
    RANGE: 0.1,
    ENEMY_SAVE: test_armour,
}

# for ws in warscrolls:
#     ws.simplest_stats(context, front_size=145)

print(attack_round(value(2), Roll(4), Roll(4), value(-1), value(1), [], context))
