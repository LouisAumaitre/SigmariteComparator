from sigmar.basics.base import infantry
from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import ENEMY_BASE, ENEMY_NUMBERS
from sigmar.compendium.seraphon import saurus_warriors, skinks, kroxigors


def test_saurus_stats():
    # given
    context = {
        ENEMY_BASE: infantry,
        ENEMY_NUMBERS: 10,
    }
    clubs = saurus_warriors.units['Celestite Club, Powerful Jaws and Stardrake Shield']
    spears = saurus_warriors.units['Celestite Spear, Powerful Jaws and Stardrake Shield']
    # assert
    assert round(clubs.average_damage(Roll(4), context, nb=1), 2) == 0.25
    assert round(spears.average_damage(Roll(4), context, nb=1), 2) == 0.21
    assert round(clubs.average_damage(Roll(4), context, nb=10), 2) == 2.5
    assert round(spears.average_damage(Roll(4), context, nb=10), 2) == 2.08
    assert round(clubs.average_damage(Roll(4), context, nb=20), 2) == 6.94
    assert round(spears.average_damage(Roll(4), context, nb=20), 2) == 5.83
    assert round(clubs.average_damage(Roll(4), context, nb=30), 2) == 17.08
    assert round(spears.average_damage(Roll(4), context, nb=30), 2) == 13.75


def test_skinks_stats():
    # given
    context = {
        ENEMY_BASE: infantry,
        ENEMY_NUMBERS: 10,
    }
    jav = skinks.units['Meteoritic Javelin, Star-buckler']
    bolt = skinks.units['Boltsplitter, Star-buckler']
    bolt_club = skinks.units['Boltsplitter, Moonstone Club']
    club = skinks.units['Moonstone Club, Star-buckler']
    # assert
    assert round(jav.average_damage(Roll(4), context, nb=1), 2) == 0.11
    assert round(bolt.average_damage(Roll(4), context, nb=1), 2) == 0.08
    assert round(bolt_club.average_damage(Roll(4), context, nb=10), 2) == 1.67
    assert round(club.average_damage(Roll(4), context, nb=10), 2) == 0.83
    assert round(jav.average_damage(Roll(4), context, nb=20, _range=5), 2) == 2.5
    assert round(bolt.average_damage(Roll(4), context, nb=20, _range=5), 2) == 1.67
    assert round(jav.average_damage(Roll(4), context, nb=30, _range=5), 2) == 5
    assert round(bolt.average_damage(Roll(4), context, nb=30, _range=5), 2) == 3.33


def test_kroxigor_stats():
    # given
    context = {
        ENEMY_BASE: infantry,
        ENEMY_NUMBERS: 10,
    }
    krok = kroxigors.units['Drakebite Maul, Vice-like Jaws']
    # assert
    assert round(krok.average_damage(Roll(4), context, nb=1), 2) == 1.51
    assert round(krok.average_damage(Roll(4), context, nb=1, _range=1.5), 2) == 1.33
