from sigmar.basics.base import large_infantry_base, monster_base
from sigmar.basics.rules import Rule, CommandAbility
from sigmar.basics.string_constants import MW_ON_HIT_CRIT, CHARGING
from sigmar.basics.unit import WeaponRule
from sigmar.basics.unit_rules import reroll_1_save, fly
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.basics.weapon_rules import reroll_1_tohit, plus_1_tohit_5_wounds, d3_extra_attacks_in_charge
from sigmar.compendium.generic_keywords import ORDER, HUMAN, CELESTIAL, HERO

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

dracoth_claws_and_fangs = Weapon('Dracoth`s Claws and Fangs', 1, 3, 3, 3, -1, 1, [])


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
        [Weapon('Tempestos Hammer', 2, 3, 3, 2, -1, 'D3', [Rule('', d3_extra_attacks_in_charge)]),
         dracoth_claws_and_fangs],
    ], 10, 3, 9, 7, 1, monster_base, rules=[
        Rule('Retribution from on High', lambda x: None),
        CommandAbility('Lord of the Host', None),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, HERO]))

STORMCAST_WS.append(Warscroll(
    'Liberators', [
        [Weapon('Warhammer', 1, 2, 4, 3, 0, 1, []), sigmarite_shields],
        [Weapon('Warblade', 1, 2, 3, 4, 0, 1, []), sigmarite_shields],
        [Weapon('Warhammers', 1, 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Warblades', 1, 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
    ], 5, 4, 6, 2, 5, large_infantry_base, rules=[
        WeaponRule('Lay low the Tyrants', plus_1_tohit_5_wounds),
    ], keywords=[ORDER, CELESTIAL, HUMAN, STORMCAST_ETERNAL, REDEEMER]))

stormcasts_by_name = {unit.name: unit for unit in STORMCAST_WS}
