from sigmar.basics.base import infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import ENEMY_BASE, ENEMY_NUMBERS, ENEMY_SAVE, SELF_NUMBERS, RANGE
from sigmar.compendium.seraphon import seraphons_by_name


def test_saurus_stats():
    # given
    context = {
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
    }
    clubs = seraphons_by_name['Saurus Warriors'].units['Celestite Club']
    spears = seraphons_by_name['Saurus Warriors'].units['Celestite Spear']
    # assert
    assert round(clubs.average_damage(context), 2) == 0.25
    assert round(spears.average_damage(context), 2) == 0.21
    context[SELF_NUMBERS] = 10
    assert round(clubs.average_damage(context), 2) == 2.5
    assert round(spears.average_damage(context), 2) == 2.08
    context[SELF_NUMBERS] = 20
    assert round(clubs.average_damage(context), 2) == 6.94
    assert round(spears.average_damage(context), 2) == 5.83
    context[SELF_NUMBERS] = 30
    assert round(clubs.average_damage(context), 2) == 17.08
    assert round(spears.average_damage(context), 2) == 13.75


def test_skinks_stats():
    # given
    context = {
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
    }
    jav = seraphons_by_name['Skinks'].units['Meteoritic Javelin, Star-buckler']
    bolt = seraphons_by_name['Skinks'].units['Boltspitter, Star-buckler']
    bolt_club = seraphons_by_name['Skinks'].units['Boltspitter, Moonstone Club']
    club = seraphons_by_name['Skinks'].units['Moonstone Club, Star-buckler']
    # assert
    assert round(jav.average_damage(context), 2) == 0.03
    assert round(bolt.average_damage(context), 2) == 0.03
    context[SELF_NUMBERS] = 10
    assert round(bolt_club.average_damage(context), 2) == 1.11
    assert round(club.average_damage(context), 2) == 0.83
    context[SELF_NUMBERS] = 20
    context[RANGE] = 5
    assert round(jav.average_damage(context), 2) == 2.5
    assert round(bolt.average_damage(context), 2) == 1.67
    context[SELF_NUMBERS] = 30
    context[RANGE] = 5
    assert round(jav.average_damage(context), 2) == 5
    assert round(bolt.average_damage(context), 2) == 3.33


def test_kroxigor_stats():
    # given
    context = {
        ENEMY_BASE: infantry_base,
        ENEMY_NUMBERS: 10,
        ENEMY_SAVE: Roll(4),
        SELF_NUMBERS: 1,
        RANGE: 0.1
    }
    krok = seraphons_by_name['Kroxigors'].units['']
    # assert
    assert round(krok.average_damage(context), 2) == 1.61
    context[RANGE] = 1.5
    assert round(krok.average_damage(context), 2) == 1.33
