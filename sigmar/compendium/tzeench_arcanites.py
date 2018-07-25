from sigmar.basics.base import monster_base, large_infantry_base, infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule, Spell, CommandAbility, TodoRule, CommentRule
from sigmar.basics.string_constants import UNBIND_RANGE, DEPLOYMENT, SELF_NUMBERS, FEAR
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import fly, can_reroll_x_dice_during_game, can_steal_spells, copy_spells
from sigmar.basics.value import value, RandomValue, OncePerGame
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import extra_damage_on_keyword, deal_x_mortal_wound_on_roll, d3_mw_on_4_if_wounded
from sigmar.compendium.generic_keywords import CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER

TZEENTCH_WS = []

HORROR = 'HORROR'
FLAMER = 'FLAMER'


def mastery_of_magic(u: Unit):
    # when casting/unbinding a spell, the lowest dice becomes equal to the highest
    u.casting_value = RandomValue({2: 1/36, 4: 3/36, 6: 5/36, 8: 7/36, 10: 9/36, 12: 11/36})
    u.unbinding_value = RandomValue({2: 1/36, 4: 3/36, 6: 5/36, 8: 7/36, 10: 9/36, 12: 11/36})


TZEENTCH_WS.append(Warscroll(
    'Lord of Change', [
        [Weapon('Rod of Sorcery', 18, '2D6', 3, 3, 0, 1, []),
         Weapon('Staff of Tzeentch', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
        [Weapon('Staff of Tzeentch', 3, 3, 4, {11: 2, 5: 3, 0: 4}, 0, 2, []),
         Weapon('Baleful Sword', 1, 2, 4, 2, -2, 3, []),
         Weapon('Curved Beak and Wicked Talons', 1, 4, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', mastery_of_magic),
        Rule('Spell-thief', can_steal_spells(UNBIND_RANGE, RandomValue({1: 5/9, 0: 4/9}), 2)),
        CommandAbility('Beacon of Sorcery', None),
        Spell('Infernal Gateway', 7, None),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER], cast=2, unbind=2))


TZEENTCH_WS.append(Warscroll(
    'Kairos Fateweaver', [
        [Weapon('Staff of Tomorrow', 3, 2, 4, {11: 2, 5: 3, 0: 4}, -1, 2, []),
         Weapon('Beaks and Talons', 1, 5, 4, 3, -1, 2, [])],
    ], {11: 10, 8: 9, 5: 8, 2: 7, 0: 6}, 4, 10, 14, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Mastery of Magic', mastery_of_magic),
        Rule('Oracle of Eternity', can_reroll_x_dice_during_game(1)),
        Spell('Gift of Change', 8, None),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER, 'LORD OF CHANGE'], cast=2, unbind=2, named=True))


def arcane_tome(u: Unit):
    u.casting_value = u.casting_value + OncePerGame('D6')


sky_sharks = Rule('Sky-sharks', extra_damage_on_keyword(value('D3') - 1, MONSTER))

TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch on Burning Chariot', [
        [Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Wake of Fire', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll('D3', Roll(4)))]),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [sky_sharks])],
        [Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Wake of Fire', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll('D3', Roll(4)))]),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [sky_sharks])],
    ], 14, 5, 10, 8, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Arcane Tome', arcane_tome),
        Spell('Tzeentch`s Firestorm', 9, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO, 'HERALD ON CHARIOT'], cast=1, unbind=1))


TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch on Disc', [
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
    ], 16, 5, 10, 5, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
        Rule('Arcane Tome', arcane_tome),
        Spell('Blue Fire of Tzeentch', 4, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO, 'HERALD ON DISC'], cast=1, unbind=1))


TZEENTCH_WS.append(Warscroll(
    'The Changeling', [
        [Weapon('The Trickster`s Staff', 2, 1, 4, 3, -1, 'D3', [])],
    ], 5, 5, 10, 5, 1, infantry_base, rules=[
        CommentRule('Arch-Deceiver', DEPLOYMENT),
        TodoRule('Puckish Misdirection'),
        TodoRule('Formless Horror'),
        Rule('', copy_spells(9))
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1, named=True))


def fortune_and_fate(u: Unit):
    # when casting a spell, any roll of 9 or more gives an extra spell
    potential_cast = u.casting_value.potential_values({})
    one = sum([proba for cast, proba in potential_cast if cast < 9])
    two = sum([proba for cast, proba in potential_cast if cast >= 9])
    three = two * two
    u.spells_per_turn = RandomValue({
        1: one,
        2: two - three,
        3: three
    })


TZEENTCH_WS.append(Warscroll(
    'Herald of Tzeentch', [
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', [])],
        [Weapon('Magical Flames', 18, 2, 4, 4, 0, 1, []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, [])],
    ], 5, 5, 10, 5, 1, infantry_base, rules=[
        Rule('Arcane Tome', arcane_tome),
        Rule('Fortune and Fate', fortune_and_fate),
        Spell('Pink Fire of Tzeentch', 9, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))


def scrolls_of_sorcery(u: Unit):
    u.casting_value = RandomValue({0: 1/6, 9: 5/6})


TZEENTCH_WS.append(Warscroll(
    'The Blue Scribes', [
        [Weapon('Sharpened Quills', 1, 2, 5, 5, 0, 1, []),
         Weapon('Disc`s Many-fanged Mouths', 1, 'D3', 4, 4, 0, 1, [])],
    ], 16, 5, 10, 5, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
        Rule('Frantic Scribbling', can_steal_spells(18, RandomValue({1: 0.5, 0: 0.5}), 3)),  # tries illimited?
        Rule('Scrolls of Sorcery', scrolls_of_sorcery),
        Spell('Boon of Tzeentch', 4, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1, named=True))


TZEENTCH_WS.append(Warscroll(
    'Screamers of Tzeentch', [
        [Weapon('Lamprey Bite', 1, 3, 4, 3, 0, 1, [sky_sharks]),
         Weapon('Slashing Fins', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll(1, Roll(6)))])],
    ], 16, 5, 10, 3, 3, large_infantry_base, rules=[
        Rule('Fly', fly),
        TodoRule('Locus of Change'),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, 'SCREAMERS']))

capricious_warpflame = Rule('Capricious Warpflame', d3_mw_on_4_if_wounded)

TZEENTCH_WS.append(Warscroll(
    'Burning Chariots of Tzeentch', [
        [Weapon('Billowing Warpflame', 18, 6, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 2, 4, 5, 3, 0, 1, []),
         Weapon('Blue Horrors` Jabs', 1, 3, 5, 5, 0, 1, []),
         Weapon('Wake of Fire', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll('D3', Roll(4)))]),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [sky_sharks])],
    ], 14, 5, 10, 6, 1, monster_base, rules=[
        Rule('Fly', fly),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, FLAMER]))

TZEENTCH_WS.append(Warscroll(
    'Exalted Flamers of Tzeentch', [
        [Weapon('Billowing Warpflame', 18, 6, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 2, 4, 5, 3, 0, 1, [])],
    ], 9, 5, 10, 4, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
    ], keywords=[CHAOS, DAEMON, FLAMER, TZEENTCH]))

TZEENTCH_WS.append(Warscroll(
    'Flamers of Tzeentch', [
        [Weapon('Warpflame', 18, 3, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 1, 2, 5, 3, 0, 1, [])],
    ], 9, 5, 10, 2, 3, infantry_base, rules=[
        Rule('Fly', fly),
        TodoRule('Locus of Transmogrification'),
    ], keywords=[CHAOS, DAEMON, FLAMER, TZEENTCH],
    special_options=[
        {'name': 'Pyrocaster', 'weapons': [
            Weapon('Warpflame', 18, 4, 4, 3, 0, 'D3', [capricious_warpflame]),
            Weapon('Flaming Maw', 1, 2, 5, 3, 0, 1, [])]}
    ]))


def flickering_flames(w: Weapon):
    def buff(data):
        if data.get(SELF_NUMBERS, 1) >= 20:
            return 1, 0
        return 0, 0
    w.tohit.rules.append(buff)


def deamon_icon_bearer(u: Unit):
    u.morale_roll = RandomValue({
        6: 1/6, 5: 1/6, 4: 1/6, 3: 1/6, 2: 1/6,
        -1: 1/36, -2: 1/36, -3: 1/36, -4: 1/36, -5: 1/36, -6: 1/36})


TZEENTCH_WS.append(Warscroll(
    'Pink Horrors of Tzeentch', [
        [Weapon('Magical Flames', 18, 1, 4, 4, 0, 1, [Rule('Flickering Flames', flickering_flames)]),
         Weapon('Grasping Hands', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 5, 10, 1, 10, infantry_base, rules=[
        Rule('Icon Bearer', deamon_icon_bearer),
        CommentRule('Hornblower', FEAR),
        TodoRule('Locus of Conjuration'),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, 'PINK HORRORS'],
    special_options=[
        {'name': 'Iridescent Horror', 'weapons': [
            Weapon('Magical Flames', 18, 1, 4, 4, 0, 1, [Rule('Flickering Flames', flickering_flames)]),
            Weapon('Grasping Hands', 1, 2, 5, 4, 0, 1, [])]}
    ]))

tzeentchites_by_name = {unit.name: unit for unit in TZEENTCH_WS}
