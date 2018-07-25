from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import CHARGING, ENEMY_BASE, ENEMY_NUMBERS, ENEMY_SAVE, SELF_NUMBERS
from sigmar.compendium.sylvaneth import sylvaneth_by_name


def test_dryad_stats():
    # given
    context = {
        CHARGING: False,
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
    }
    dryads = sylvaneth_by_name['Dryads'].units['']
    # assert
    assert round(dryads.average_damage(context), 2) == 0.25
    assert round(dryads.average_health(context), 2) == 1.5
    context[SELF_NUMBERS] = 12
    assert round(dryads.average_health(context), 2) == 24
