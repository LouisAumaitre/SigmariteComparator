from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import CHARGING, ENEMY_BASE, ENEMY_NUMBERS, ENEMY_WOUNDS
from sigmar.compendium.stormcast_eternals import liberators


def test_liberators_stats():
    # given
    context = {
        CHARGING: False,
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
    }
    context2 = {
        CHARGING: False,
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_WOUNDS: 5,
    }
    shield_libs = liberators.units['Warhammer, Sigmarite shields']
    # assert
    assert round(shield_libs.average_damage(Roll(4), context, nb=1), 2) == 0.33
    assert round(shield_libs.average_damage(Roll(4), context2, nb=1), 2) == 0.44
