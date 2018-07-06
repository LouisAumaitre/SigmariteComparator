from typing import List, Union, Tuple, Callable, Dict

from sigmar.basics.value import Value, value
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import (
    TOWOUND_MOD_ON_CRIT_HIT,
    BONUS_REND,
    CRIT_BONUS_REND,
    MW_ON_HIT_CRIT,
    MW_ON_WOUND_CRIT,
    EXTRA_HIT_ON_CRIT,
    EXTRA_WOUND_ON_CRIT,
    WEAPON_RANGE,
    EXTRA_DAMAGE_ON_CRIT_WOUND)


class Weapon:
    def __init__(
            self,
            name: str,
            range_: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            attacks: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            tohit,
            towound,
            rend,
            wounds: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            rules: List[Rule],
    ):
        self.name = name
        self.range = value(range_)
        self.attacks = value(attacks)
        self.tohit = Roll(tohit)
        self.towound = Roll(towound)
        self.rend = rend
        self.wounds = value(wounds)

        self.attack_rules: List[Callable] = []

        self.rules = rules
        for r in rules:
            r.apply(self)

    def average_hits(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.tohit.average(dices, extra_data, mod)

    def average_wounds(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.towound.average(dices, extra_data, mod)

    def unsaved_chances(self, armour: Roll, extra_rend=0) -> float:
        chances, crit = armour.chances({}, mod=self.rend + extra_rend)
        return 1 - chances - crit

    def average_damage(self, armour: Roll, data: dict, _range=1):
        if _range > self.range.average(data) or self.range.average(data) > 3 >= _range:
            return 0
        data[WEAPON_RANGE] = self.range.average(data)
        for rule in self.attack_rules:
            rule(data)
        mortal_wounds = 0

        attacks = self.attacks.average(data)
        hits, critic_hits = self.average_hits(attacks, data)
        hits += critic_hits * data.get(EXTRA_HIT_ON_CRIT, 0)

        wounds, critic_wounds = self.average_wounds(hits, data)
        _wounds, _critic_wounds = self.average_wounds(critic_hits, data, mod=data.get(TOWOUND_MOD_ON_CRIT_HIT, 0))
        wounds += _wounds
        critic_wounds += _critic_wounds
        wounds += critic_wounds * data.get(EXTRA_WOUND_ON_CRIT, 0)

        unsaved = wounds * self.unsaved_chances(armour, extra_rend=data.get(BONUS_REND, 0))
        unsaved += critic_wounds * self.unsaved_chances(
            armour, extra_rend=data.get(BONUS_REND, 0) + data.get(CRIT_BONUS_REND, 0))

        mortal_wounds += data.get(MW_ON_HIT_CRIT, 0) * critic_hits + data.get(MW_ON_WOUND_CRIT, 0) * critic_wounds
        if wounds == 0:
            print(f'{self.name}: no wounds')
            damage_per_hit = self.wounds.average(data)
        else:
            damage_per_hit = self.wounds.average(data)\
                             + data.get(EXTRA_DAMAGE_ON_CRIT_WOUND, 0) * critic_wounds / wounds
        damage = unsaved * damage_per_hit + mortal_wounds

        return damage
