from sigmar.compendium.generic_keywords import CELESTIAL, ORDER

STORMCAST_ETERNAL = 'STORMCAST ETERNAL'
REDEEMER = 'REDEEMER'

sigmarite_shields = Rule('Sigmarite shields', reroll_1_save)

liberators = Warscroll(
    'Liberators', [
        [Weapon('Warhammer', 1, 2, 4, 3, 0, 1, []), sigmarite_shields],
        [Weapon('Warblade', 1, 2, 3, 4, 0, 1, []), sigmarite_shields],
        [Weapon('Warhammers', 1, 2, 4, 3, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
        [Weapon('Warblades', 1, 2, 3, 4, 0, 1, [Rule('Paired weapons', reroll_1_tohit)])],
    ], 5, 4, 6, 2, [
        WeaponRule('Lay low the Tyrants', plus_1_tohit_5_wounds),
    ], [ORDER, CELESTIAL, DAEMON, STORMCAST_ETERNAL, REDEEMER, 'LIBERATORS'])