from sigmar.basics.base import infantry
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import (
    CHARGING, ENEMY_BASE, ENEMY_NUMBERS, REND, ENEMY_KEYWORDS, RANGE,
    ENEMY_SAVE,
)
from sigmar.compendium.generic_keywords import DAEMON, CHAOS
from sigmar.compendium.sylvaneth import SYLVANETH_WS

warscrolls = SYLVANETH_WS

test_armour = Roll(4)
context = {
    CHARGING: False,
    ENEMY_BASE: infantry,
    ENEMY_NUMBERS: 10,
    REND: -1,
    ENEMY_KEYWORDS: [CHAOS, DAEMON],
    RANGE: 0.1,
    ENEMY_SAVE: test_armour,
}

for ws in warscrolls:
    ws.simplest_stats(context, front_size=145)
