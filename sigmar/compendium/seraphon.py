from sigmar.basics.rules import Rule
from sigmar.basics.unit_rules import ignore_1_rend
from sigmar.basics.warscroll import Warscroll
from sigmar.basics.weapon import Weapon
from sigmar.compendium.generic_keywords import CELESTIAL, ORDER, DAEMON

SERAPHON = 'SERAPHON'
SAURUS = 'SAURUS'

saurus_warriors = Warscroll(
    'Saurus warriors', [
        [Weapon('Celestiste Club', 1, 1, 4, 3, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
        [Weapon('Celestite Spear', 2, 1, 4, 4, 0, 1, []),
         Weapon('Powerful Jaws and Stardrake Shield', 1, 1, 5, 4, 0, 1, [])],
    ], 5, 5, 10, 1, 10, 25, [
        Rule('Stardrake Shield', ignore_1_rend),
        Rule('Ordered Cohort', lambda x: None),
    ], [ORDER, CELESTIAL, DAEMON, SERAPHON, SAURUS, 'SAURUS WARRIORS'])
