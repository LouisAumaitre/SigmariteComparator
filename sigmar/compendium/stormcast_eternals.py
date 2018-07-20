from sigmar.basics.base import large_infantry_base, monster_base
from sigmar.basics.rules import Rule, CommandAbility
from sigmar.basics.string_constants import MW_ON_HIT_CRIT, CHARGING
from sigmar.basics.unit import WeaponRule
from sigmar.basics.unit_rules import reroll_1_save, fly
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import (
    reroll_1_tohit, extra_attacks_in_charge,
    d6_dmg_on_crit, extra_3_rend_on_crit_hit, plus_x_tohit_y_wounds
)
from sigmar.compendium.generic_keywords import ORDER, HUMAN, CELESTIAL, HERO, TOTEM

STORMCAST_WS = []

STORMCAST_ETERNAL = 'STORMCAST ETERNAL'
REDEEMER = 'REDEEMER'

sigmarite_shields = Rule('Sigmarite shields', reroll_1_save)

STORMCAST_WS.append(Warscroll(
    'Celestant-Prime', [
        [Weapon('Comet-strike Scepter', 24, 1, 1, 1, -6, 'D3', []),
         Weapon('Ghal Maraz, the Hammer of Sigmar', 2, 2, 3, 2, -3, 3, [])],
    ], 12, 3, 10, 8, 1, monster_base, rules=[
        Rule('Fly', fly),
        Rule('Retribution from on High', lambda x: None),
        Rule('Orrery of Celestial Fates', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

dracoth_claws_and_fangs = Weapon('Dracoth`s Claws and Fangs', 1, 3, 3, 3, -1, 1, [
    Rule('Intolerable_damage', d6_dmg_on_crit)])


def lightning_hammer(w: Weapon):
    # TODO: add stun
    def buff(data: dict):
        data[MW_ON_HIT_CRIT] = data.get(MW_ON_HIT_CRIT, 0) + 2
    w.attack_rules.append(buff)


def stormstrike_glaive(w: Weapon):
    def extra_damage(data):
        if data.get(CHARGING, False):
            return 1
        return 0

    def extra_rend(data):
        if data.get(CHARGING, False):
            return -1
        return 0
    w.damage.rules.append(extra_damage)
    w.rend.rules.append(extra_rend)


STORMCAST_WS.append(Warscroll(
    'Lord-Celestant on Dracoth', [
        [Weapon('Stormstrike Glaive', 2, 4, 3, 4, -1, 1, [Rule('', stormstrike_glaive)]), dracoth_claws_and_fangs],
        [Weapon('Lightning Hammer', 1, 3, 3, 3, -1, 2, [Rule('', lightning_hammer)]), dracoth_claws_and_fangs],
        [Weapon('Thunderaxe', 2, 3, 3, 3, -1, 2, [Rule('', lambda x: None)]), dracoth_claws_and_fangs],
        [Weapon('Tempestos Hammer', 2, 3, 3, 2, -1, 'D3', [Rule('', extra_attacks_in_charge('D3'))]),
         dracoth_claws_and_fangs],
    ], 10, 3, 9, 7, 1, monster_base, rules=[
        Rule('Retribution from on High', lambda x: None),
        Rule('Storm Breath', lambda x: None),
        CommandAbility('Lord of the Host', None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Lord-Celestant', [
        [Weapon('Sigmarite Runeblade', 1, 4, 3, 3, -1, 1, []),
         Weapon('Warhammer', 1, 2, 4, 3, 0, 1, [])],
    ], 5, 3, 9, 5, 1, large_infantry_base, rules=[
        WeaponRule('Inescapable Vengeance', extra_attacks_in_charge(1)),
        Rule('Sigmarite Warcloak', lambda x: None),
        CommandAbility('Furious Retribution', None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Lord-Castellant', [
        [Weapon('Castellant`s Halberd', 2, 3, 3, 3, -1, 2, [])],
    ], 5, 3, 9, 6, 1, large_infantry_base, rules=[
        Rule('Warding Lantern', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Lord-Relictor', [
        [Weapon('Relic Hammer', 1, 4, 3, 3, -1, 1, [])],
    ], 5, 3, 9, 5, 1, large_infantry_base, rules=[
        Rule('Lightning Storm', lambda x: None),
        Rule('Healing Storm', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Knight-Azyros', [
        [Weapon('Starblade', 1, 4, 3, 3, -1, 1, [])],
    ], 12, 3, 9, 5, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
        Rule('Leader of the Way', lambda x: None),
        Rule('Illuminator of the Lost', lambda x: None),
        Rule('The Light of Sigmar', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Knight-Venator', [
        [Weapon('Realmhunter`s Bow', 30, 3, 2, 3, -1, 1, []),
         Weapon('Star-eagle`s Celestial Talons', 30, 3, 4, 3, 0, 1, [Rule('', extra_3_rend_on_crit_hit)]),
         Weapon('Star-eagle`s Celestial Talons', 1, 3, 4, 3, 0, 1, [Rule('', extra_3_rend_on_crit_hit)])],
    ], 12, 3, 9, 5, 1, large_infantry_base, rules=[
        Rule('Fly', fly),
        Rule('Star-fated Arrow', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Knight-Vexillor', [
        [Weapon('Warhammer', 1, 4, 4, 3, 0, 1, []), Rule('Meteoritic Standard', lambda x: None)],
        [Weapon('Warhammer', 1, 4, 4, 3, 0, 1, []), Rule('Pennant of the Stormbringer', lambda x: None)],
    ], 4, 3, 9, 5, 1, large_infantry_base, rules=[
        Rule('Icon of War', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO, TOTEM]))

STORMCAST_WS.append(Warscroll(
    'Knight-Heraldor', [
        [Weapon('Sigmarite Broadsword', 1, 4, 3, 4, -1, 1, [])],
    ], 5, 4, 8, 5, 1, large_infantry_base, rules=[
        Rule('Onward to Glory', lambda x: None),
        Rule('Thunderblast', lambda x: None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Liberators', [
        [Weapon('Warhammer', 1, 2, 4, 3, 0, 1, []), sigmarite_shields],
        [Weapon('Warblade', 1, 2, 3, 4, 0, 1, []), sigmarite_shields],
        [Weapon('Warhammers', 1, 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Warblades', 1, 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
    ], 5, 4, 6, 2, 5, large_infantry_base, rules=[
        WeaponRule('Lay low the Tyrants', plus_x_tohit_y_wounds(1, 5)),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, REDEEMER],
    special_options=[
        {'name': 'Liberator-Prime',
         'weapons': [Weapon('Warhammer', 1, 3, 4, 3, 0, 1, [])], 'rules': [sigmarite_shields]},
        {'name': 'Liberator-Prime',
         'weapons': [Weapon('Warblade', 1, 2, 3, 4, 0, 1, [])], 'rules': [sigmarite_shields]},
        {'name': 'Liberator-Prime',
         'weapons': [Weapon('Warhammers', 1, 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])]},
        {'name': 'Liberator-Prime',
         'weapons': [Weapon('Warblades', 1, 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])]},
        {'type': 'special weapon',
         'weapons': [Weapon('Grandhammer', 1, 2, 4, 3, -1, 2, [])]},
        {'type': 'special weapon',
         'weapons': [Weapon('Grandblade', 1, 2, 3, 4, -1, 2, [])]},
    ]))

# at the end
stormcasts_by_name = {unit.name: unit for unit in STORMCAST_WS}
