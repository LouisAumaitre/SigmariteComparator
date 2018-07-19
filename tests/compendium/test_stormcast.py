from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import CHARGING, ENEMY_BASE, ENEMY_NUMBERS, ENEMY_WOUNDS, ENEMY_SAVE, SELF_NUMBERS
from sigmar.compendium.stormcast_eternals import stormcasts_by_name


def test_liberators_stats():
    # given
    context = {
        CHARGING: False,
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
    }
    context2 = {
        CHARGING: False,
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_WOUNDS: 5,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
    }
    shield_libs = stormcasts_by_name['Liberators'].units['Warhammer, Sigmarite shields']
    # assert
    assert round(shield_libs.average_damage(context), 2) == 0.33
    assert round(shield_libs.average_damage(context2), 2) == 0.44
