from sigmar.basics.base import monster_base, large_infantry_base, infantry_base
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule, Spell, CommandAbility, TodoRule, CommentRule
from sigmar.basics.string_constants import UNBIND_RANGE, DEPLOYMENT, SELF_NUMBERS, FEAR, ENEMY_BRAVERY, ENEMY_WOUNDS, \
    SELF_WOUNDS
from sigmar.basics.unit import Unit
from sigmar.basics.unit_rules import fly, can_reroll_x_dice_during_game, can_steal_spells, copy_spells, extra_save, \
    regeneration, run_and_charge, FLIGHT
from sigmar.basics.value import value, RandomValue, OncePerGame
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import extra_damage_on_keyword, deal_x_mortal_wound_on_roll, d3_mw_on_4_if_wounded, \
    impact_x_mortal_wound, deal_x_mortal_wound_crit_tohit
from sigmar.compendium.generic_keywords import CHAOS, DAEMON, TZEENTCH, WIZARD, HERO, MONSTER, GOR, MORTAL, EVERCHOSEN

TZEENTCH_WS = []

HORROR = 'HORROR'
FLAMER = 'FLAMER'
ARCANITE = 'ARCANITE'


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
        FLIGHT,
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
        FLIGHT,
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
        FLIGHT,
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
        FLIGHT,
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
        FLIGHT,
        Rule('Frantic Scribbling', can_steal_spells(18, RandomValue({1: 0.5, 0: 0.5}), 3)),  # tries illimited?
        Rule('Scrolls of Sorcery', scrolls_of_sorcery),
        Spell('Boon of Tzeentch', 4, None),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, WIZARD, HERO], cast=1, unbind=1, named=True))


TZEENTCH_WS.append(Warscroll(
    'Screamers of Tzeentch', [
        [Weapon('Lamprey Bite', 1, 3, 4, 3, 0, 1, [sky_sharks]),
         Weapon('Slashing Fins', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll(1, Roll(6)))])],
    ], 16, 5, 10, 3, 3, large_infantry_base, rules=[
        FLIGHT,
        TodoRule('Locus of Change'),
    ], keywords=[CHAOS, DAEMON, TZEENTCH, 'SCREAMERS'], max_size=9))

capricious_warpflame = Rule('Capricious Warpflame', d3_mw_on_4_if_wounded)

TZEENTCH_WS.append(Warscroll(
    'Burning Chariots of Tzeentch', [
        [Weapon('Billowing Warpflame', 18, 6, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 2, 4, 5, 3, 0, 1, []),
         Weapon('Blue Horrors` Jabs', 1, 3, 5, 5, 0, 1, []),
         Weapon('Wake of Fire', 'move across', 1, 7, 7, 0, 0, [Rule('', deal_x_mortal_wound_on_roll('D3', Roll(4)))]),
         Weapon('Screamer`s Lamprey Bites', 1, 6, 4, 3, 0, 1, [sky_sharks])],
    ], 14, 5, 10, 6, 1, monster_base, rules=[
        FLIGHT,
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, FLAMER], max_size=3))

TZEENTCH_WS.append(Warscroll(
    'Exalted Flamers of Tzeentch', [
        [Weapon('Billowing Warpflame', 18, 6, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 2, 4, 5, 3, 0, 1, [])],
    ], 9, 5, 10, 4, 1, large_infantry_base, rules=[
        FLIGHT,
    ], keywords=[CHAOS, DAEMON, FLAMER, TZEENTCH], max_size=3))

TZEENTCH_WS.append(Warscroll(
    'Flamers of Tzeentch', [
        [Weapon('Warpflame', 18, 3, 4, 3, 0, 'D3', [capricious_warpflame]),
         Weapon('Flaming Maw', 1, 2, 5, 3, 0, 1, [])],
    ], 9, 5, 10, 2, 3, infantry_base, rules=[
        FLIGHT,
        TodoRule('Locus of Transmogrification'),
    ], keywords=[CHAOS, DAEMON, FLAMER, TZEENTCH], max_size=9,
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
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, 'PINK HORRORS'], max_size=40,
    special_options=[
        {'name': 'Iridescent Horror', 'weapons': [
            Weapon('Magical Flames', 18, 1, 4, 4, 0, 1, [Rule('Flickering Flames', flickering_flames)]),
            Weapon('Grasping Hands', 1, 2, 5, 4, 0, 1, [])]}
    ]))


TZEENTCH_WS.append(Warscroll(
    'Blue Horrors of Tzeentch', [
        [Weapon('Magical Flames', 14, 1, 4, 4, 0, 1, []),
         Weapon('Taloned Hands', 1, 1, 5, 5, 0, 1, [])],
    ], 5, 6, 10, 1, 10, infantry_base, rules=[
        TodoRule('Split'),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, 'BLUE HORRORS'], max_size=40))


TZEENTCH_WS.append(Warscroll(
    'Brimstone Horrors of Tzeentch', [
        [Weapon('Magical Flames', 12, 2, 5, 5, 0, 1, []),
         Weapon('Taloned Hands', 1, 2, 5, 6, 0, 1, [])],
    ], 5, 7, 10, 1, 10, infantry_base, rules=[
        TodoRule('Split Again'),
    ], keywords=[CHAOS, DAEMON, HORROR, TZEENTCH, 'BRIMSTONE HORRORS'], max_size=40))


def sorcerous_elixir(u: Unit):
    u.spells_per_turn = u.spells_per_turn + OncePerGame(1)
    # TODO: add reroll once per game


TZEENTCH_WS.append(Warscroll(
    'Tzaangor Shaman', [
        [Weapon('Staff of Change', 2, 1, 4, 3, -1, 'D3', []),
         Weapon('Ritual Dagger', 1, 2, 4, 4, 0, 1, []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
    ], 16, 5, 6, 6, 1, large_infantry_base, rules=[
        FLIGHT,
        Rule('Sorcerous Elixir', sorcerous_elixir),
        Spell('Boon of Mutation', 7, None),
    ], keywords=[CHAOS, GOR, ARCANITE, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))


TZEENTCH_WS.append(Warscroll(
    'Curseling, Eye of Tzeentch', [
        [Weapon('Blazing Sword', 1, 3, 3, 4, -1, 1, []),
         Weapon('Threshing Flail', 1, 3, 4, 3, 0, 1, []),
         Weapon('Staff of Tzeentch', 2, 1, 5, 4, 0, 'D3', [])],
    ], 5, 4, 7, 5, 1, infantry_base, rules=[
        CommentRule('Vessel of Chaos', 'Rebound unbound spells'),
        Spell('Glean Magic', 3, None),
    ], keywords=[CHAOS, MORTAL, ARCANITE, TZEENTCH, WIZARD, HERO], cast=2, unbind=2, named=True))


def magic_touched(u: Unit):
    # when casting a spell, any double gives an extra spell
    one = 5/6
    two = 1/6
    three = two * two
    u.spells_per_turn = RandomValue({
        1: one,
        2: two - three,
        3: three
    })


TZEENTCH_WS.append(Warscroll(
    'Magister', [
        [Weapon('Warpsteel Sword', 1, 1, 4, 4, 0, 1, []),
         Weapon('Tzeentchian Staff', 18, 1, 3, 4, 0, 'D3', [])],
    ], 6, 5, 7, 5, 1, infantry_base, rules=[
        Rule('Magic-touched', magic_touched),
        Spell('Bolt of Change', 7, None),
    ], keywords=[CHAOS, MORTAL, ARCANITE, TZEENTCH, WIZARD, HERO], cast=1, unbind=1))


def warptongue_blade(w: Weapon):
    # If a Warptongue Blade inflicts damage on an enemy unit, roll two dice. If the roll is higher than the enemy
    # unit’s Bravery, one model in the unit is slain. Otherwise, the blade inflicts 1 wound.
    def buff(data):
        enemy_wounds = data.get(ENEMY_WOUNDS, 1)
        if enemy_wounds <= 1:
            return 0
        bravery = data.get(ENEMY_BRAVERY, 7)
        roll_higher = sum([proba for val, proba in value('2D6').potential_values(data) if val > bravery])
        return RandomValue({0: 1 - roll_higher, enemy_wounds - 1: roll_higher})
    w.damage.rules.append(buff)


TZEENTCH_WS.append(Warscroll(
    'Gaunt Summoner of Tzeentch', [
        [Weapon('Warptongue Blade', 1, 1, 3, 4, 0, 1, [Rule('', warptongue_blade)]),
         Weapon('Changestaff', 18, 1, 3, 4, 0, 'D3', [])],
    ], 5, 6, 8, 5, 1, large_infantry_base, rules=[
        CommentRule('Book of Profane Secrets', 'Can summon DAEMONS through Realmgates'),
        Spell('Infernal Flames', 8, None),
    ], keywords=[CHAOS, MORTAL, DAEMON, ARCANITE, EVERCHOSEN, TZEENTCH, WIZARD, HERO, 'GAUNT SUMMONER'],
    cast=2, unbind=2))


TZEENTCH_WS.append(Warscroll(
    'Fatemaster', [
        [Weapon('Fireglaive of Tzeentch', 2, 3, 3, 4, 0, 'D3', []),
         Weapon('Disc of Tzeentch`s Protuding Blades', 1, 'D3', 4, 4, 0, 1, [])],
    ], 16, 4, 8, 6, 1, large_infantry_base, rules=[
        FLIGHT,
        Rule('Soulbound Shield', extra_save(4)),
        CommentRule('Hovering Disc of Tzeentch', '+2 save against non flyers'),
        CommandAbility('Lord of Fate', None),
    ], keywords=[CHAOS, MORTAL, DAEMON, ARCANITE, TZEENTCH, HERO]))


def brutal_rage(u: Unit):
    def buff(data):
        if data.get(SELF_WOUNDS, 8) <= 3:
            return 1, 0
        return 0, 0
    for w in u.weapons:
        w.tohit.rules.append(buff)

    def debuff(data):
        if data.get(SELF_WOUNDS, 8) <= 3:
            return -1
        return 0
    u.casting_value.rules.append(debuff)
    u.unbinding_value.rules.append(debuff)


TZEENTCH_WS.append(Warscroll(
    'Ogroid Traumaturge', [
        [Weapon('Traumaturge Staff', 2, 2, 3, 3, -1, 'D3', []),
         Weapon('Great Horns', 1, 1, 3, 3, -2, 3, []),
         Weapon('Cloven Hooves', 1, 4, 4, 3, 0, 1, []),
         Weapon('Mighty Bulk', 1, 1, 7, 7, 0, 1, [Rule('', impact_x_mortal_wound('D3'))])],
    ], 6, 5, 8, 8, 1, large_infantry_base, rules=[
        Rule('Brutal Rage', brutal_rage),
        Rule('Overwhelming Power', regeneration(1)),
        Spell('Fireblast', 7, None),
    ], keywords=[CHAOS, MORTAL, ARCANITE, TZEENTCH, HERO, WIZARD], cast=1, unbind=1))


def savagery_unleashed_func(w: Weapon):
    def buff(data):
        nb = data.get(SELF_NUMBERS)
        return min(3, nb // 9)
    w.attacks.rules.append(buff)


savagery_unleashed = Rule('Savagery Unleashed', savagery_unleashed_func)

TZEENTCH_WS.append(Warscroll(
    'Tzaangors', [
        [Weapon('Paired Savage Blades', 1, 2, 3, 4, 0, 1, [savagery_unleashed]),
         Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, [])],
        [Weapon('Savage Blade', 1, 2, 4, 4, 0, 1, [savagery_unleashed]),
         Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, []),
         Rule('Arcanite Shield', extra_save(6))],
    ], 6, 5, 5, 2, 5, infantry_base, rules=[
        TodoRule('Icon Bearers'),
        Rule('Brayhorn', run_and_charge),
        TodoRule('Anarchy and Mayhem'),
    ], keywords=[CHAOS, GOR, ARCANITE, TZEENTCH], max_size=20,
    special_options=[
        {
            'name': 'Twistbray', 'type': 'leader',
            'weapons': [
                Weapon('Paired Savage Blades', 1, 2, 2, 4, 0, 1, [savagery_unleashed]),
                Weapon('Vicious Beak', 1, 1, 3, 5, 0, 1, [])]
        }, {
            'name': 'Twistbray', 'type': 'leader', 'rules': [Rule('Arcanite Shield', extra_save(6))],
            'weapons': [
                Weapon('Savage Blade', 1, 2, 3, 4, 0, 1, [savagery_unleashed]),
                Weapon('Vicious Beak', 1, 1, 3, 5, 0, 1, [])]
        }, {
            'type': 'special weapon', 'weapons': [
                Weapon('Savage Greatblade', 1, 1, 4, 4, -1, 2, [savagery_unleashed]),
                Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, [])]
        }, {
            'name': 'Mutant', 'type': 'mutant',
            'weapons': [
                Weapon('Paired Savage Blades', 1, 3, 3, 4, 0, 1, [savagery_unleashed]),
                Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, [])]
        }
    ]))

sorcerous_bolt = Weapon('Sorcerous Bolt', 18, 1, 5, 4, 0, 1, [])  # range 12 without scroll of Dark Arts
sorcerous_bolt_2 = Weapon('Sorcerous Bolt', 18, 2, 5, 4, 0, 1, [])  # range 12 without scroll of Dark Arts

TZEENTCH_WS.append(Warscroll(
    'Kairic Acolytes', [
        [sorcerous_bolt, Weapon('Cursed Blade', 1, 1, 4, 4, 0, 1, [])],
        [sorcerous_bolt, Weapon('Cursed Blade', 1, 1, 4, 4, 0, 1, []), Rule('Arcanite Shield', extra_save(6))],
        [sorcerous_bolt, Weapon('Paired Cursed Blades', 1, 1, 3, 4, 0, 1, [])],
    ], 6, 6, 5, 1, 10, infantry_base, rules=[
        TodoRule('Scroll of Dark Arts'),
        TodoRule('Vulcharc'),
    ], keywords=[CHAOS, MORTAL, ARCANITE, TZEENTCH], max_size=30,
    special_options=[
        {
            'name': 'Kairic Adept', 'type': 'leader',
            'weapons': [sorcerous_bolt_2, Weapon('Cursed Blade', 1, 1, 4, 4, 0, 1, [])],
        }, {
            'name': 'Kairic Adept', 'type': 'leader',
            'weapons': [sorcerous_bolt_2, Weapon('Cursed Blade', 1, 1, 4, 4, 0, 1, [])],
            'rules': [Rule('Arcanite Shield', extra_save(6))],
        }, {
            'name': 'Kairic Adept', 'type': 'leader',
            'weapons': [sorcerous_bolt_2, Weapon('Paired Cursed Blades', 1, 1, 3, 4, 0, 1, [])],
        }, {
            'type': 'special weapon',
            'weapons': [sorcerous_bolt, Weapon('Double-handed Cursed Glaive', 1, 1, 4, 4, -1, 1, [])],
        }
    ]))

TZEENTCH_WS.append(Warscroll(
    'Tzaangor Enlightened', [
        [Weapon('Tzeentchian Spear', 2, 2, 4, 3, -1, 2, []),
         Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, [])],
    ], 6, 5, 6, 3, 3, infantry_base, rules=[
        CommentRule('Babbling Stream of Secrets', FEAR),
        TodoRule('Guided by the Past'),
        TodoRule('Prepernatural Enhancement'),
    ], keywords=[CHAOS, GOR, ARCANITE, TZEENTCH], max_size=9,
    special_options=[
        {
            'name': 'Aviarch', 'type': 'leader',
            'weapons': [
                Weapon('Tzeentchian Spear', 2, 3, 4, 3, -1, 2, []),
                Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, [])],
        }
    ]))

TZEENTCH_WS.append(Warscroll(
    'Tzaangor Enlightened on Discs of Tzeentch', [
        [Weapon('Tzeentchian Spear', 2, 2, 4, 3, -1, 2, []),
         Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
    ], 16, 5, 6, 4, 3, large_infantry_base, rules=[
        FLIGHT,
        CommentRule('Babbling Stream of Secrets', FEAR),
        TodoRule('Guided by the Past'),
        TodoRule('Prepernatural Enhancement'),
    ], keywords=[CHAOS, GOR, ARCANITE, TZEENTCH, DAEMON], max_size=9,
    special_options=[
        {
            'name': 'Aviarch', 'type': 'leader',
            'weapons': [
                Weapon('Tzeentchian Spear', 2, 3, 4, 3, -1, 2, []),
                Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, []),
                Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
        }
    ]))

TZEENTCH_WS.append(Warscroll(
    'Tzaangor Skyfires', [
        [Weapon('Greatbow`s Arrow of Fate', 24, 1, 4, 3, -1, 'D3', [
            Rule('Judgement from Afar', deal_x_mortal_wound_crit_tohit('D3'))]),
         Weapon('Greatbow', 1, 2, 5, 5, 0, 1, []),
         Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, []),
         Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
    ], 16, 5, 6, 4, 3, large_infantry_base, rules=[
        FLIGHT,
        CommentRule('Babbling Stream of Secrets', FEAR),
        TodoRule('Guided by the Future'),
        TodoRule('Prepernatural Enhancement'),
    ], keywords=[CHAOS, GOR, ARCANITE, TZEENTCH, DAEMON], max_size=9,
    special_options=[
        {
            'name': 'Aviarch', 'type': 'leader',
            'weapons': [
                Weapon('Greatbow`s Arrow of Fate', 24, 1, 3, 3, -1, 'D3', [
                    Rule('Judgement from Afar', deal_x_mortal_wound_crit_tohit('D3'))]),
                Weapon('Greatbow', 1, 2, 5, 5, 0, 1, []),
                Weapon('Vicious Beak', 1, 1, 4, 5, 0, 1, []),
                Weapon('Disc of Tzeentch`s Teeth and Horns', 1, 'D3', 4, 3, -1, 'D3', [])],
        }
    ]))


tzeentchites_by_name = {unit.name: unit for unit in TZEENTCH_WS}
