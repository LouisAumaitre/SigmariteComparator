from typing import List, Union, Tuple, Callable, Dict

from math import factorial

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
    EXTRA_DAMAGE_ON_CRIT_WOUND,
    RANGE,
    AUTO_WOUND_ON_CRIT,
    ENEMY_SAVE,
    EXTRA_ATTACK_ON_HIT,
    MW_ON_DAMAGE,
)


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
        self.rend = value(rend)
        self.wounds = value(wounds)
        self.extra_wounds_after_everything_else = []

        self.attack_rules: List[Callable] = []

        self.rules = rules
        for r in rules:
            r.apply(self)

    def average_hits(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.tohit.average(dices, extra_data, mod)

    def average_wounds(self, dices, extra_data: dict, mod=0) -> Tuple[float, float]:
        return self.towound.average(dices, extra_data, mod)

    def unsaved_chances(self, extra_data: dict, extra_rend=0) -> float:
        chances, crit = extra_data[ENEMY_SAVE].chances({}, mod=self.rend.average(extra_data, extra_rend))
        return 1 - chances - crit

    def average_damage(self, data: dict):
        if data.get(RANGE, 0) > self.range.average(data) or self.range.average(data) > 3 >= data.get(RANGE, 0):
            return 0
        data[WEAPON_RANGE] = self.range.average(data)
        for rule in self.attack_rules:
            rule(data)
        mortal_wounds = 0

        attacks = self.attacks.average(data)
        hits, critic_hits = self.average_hits(attacks, data)
        _hits, _critic_hits = self.average_hits(data.get(EXTRA_ATTACK_ON_HIT, 0) * (hits + critic_hits), data)
        hits += _hits
        critic_hits += _critic_hits
        hits += critic_hits * data.get(EXTRA_HIT_ON_CRIT, 0)

        wounds, critic_wounds = self.average_wounds(hits, data)
        if data.get(AUTO_WOUND_ON_CRIT, False):
            _wounds, _critic_wounds = critic_hits, 0
        else:
            _wounds, _critic_wounds = self.average_wounds(critic_hits, data, mod=data.get(TOWOUND_MOD_ON_CRIT_HIT, 0))
        wounds += _wounds
        critic_wounds += _critic_wounds
        wounds += critic_wounds * data.get(EXTRA_WOUND_ON_CRIT, 0)

        unsaved = wounds * self.unsaved_chances(data, extra_rend=data.get(BONUS_REND, 0))
        unsaved += critic_wounds * self.unsaved_chances(
            data, extra_rend=data.get(BONUS_REND, 0) + data.get(CRIT_BONUS_REND, 0))

        mortal_wounds += data.get(MW_ON_HIT_CRIT, 0) * critic_hits + data.get(MW_ON_WOUND_CRIT, 0) * critic_wounds
        mortal_wounds += data.get(MW_ON_DAMAGE, 0) * unsaved
        if wounds == 0:
            damage_per_hit = self.wounds.average(data)
        else:
            damage_per_hit = self.wounds.average(data) \
                             + data.get(EXTRA_DAMAGE_ON_CRIT_WOUND, 0) * critic_wounds / wounds
        damage = unsaved * damage_per_hit + mortal_wounds

        return damage

    def probability_of_damage(self, data: dict, users=1):
        if data.get(RANGE, 0) > self.range.average(data) or self.range.average(data) > 3 >= data.get(RANGE, 0):
            return 0
        data[WEAPON_RANGE] = self.range.average(data)
        for rule in self.attack_rules:
            rule(data)

        potential_attacks = {}
        potential_hits = {}
        potential_wounds = {}
        potential_unsaved = {}
        try:
            potential_attacks = [(nb * users, proba) for (nb, proba) in self.attacks.potential_values(data)]
            assert abs(sum([proba for (val, proba) in potential_attacks]) - 1) <= pow(0.1, 5)

            potential_hits = [
                (
                    nb, atk_proba * binomial(atk_value, nb) * (pow(self.tohit.success(data), nb) * pow(
                        self.tohit.fail(data), atk_value - nb))
                ) for (atk_value, atk_proba) in potential_attacks for nb in range(atk_value+1)
            ]
            # hits = hits + critic_hits * data.get(EXTRA_HIT_ON_CRIT, 0)
            assert abs(sum([proba for (val, proba) in potential_hits]) - 1) <= pow(0.1, 5)

            potential_wounds = [
                (
                    nb, hit_proba * binomial(hit_value, nb) * (pow(self.towound.success(data), nb) * pow(
                        self.towound.fail(data), hit_value - nb))
                ) for (hit_value, hit_proba) in potential_hits for nb in range(hit_value+1)
            ]
            # _wounds, _critic_wounds = self.average_wounds(critic_hits, data, mod=data.get(TOWOUND_MOD_ON_CRIT_HIT, 0))
            # wounds += critic_wounds * data.get(EXTRA_WOUND_ON_CRIT, 0)
            assert abs(sum([proba for (val, proba) in potential_wounds]) - 1) <= pow(0.1, 5)

            potential_unsaved = [
                (
                    nb, wnd_proba * binomial(wnd_value, nb) * (pow(data[ENEMY_SAVE].fail(data), nb) * pow(
                        data[ENEMY_SAVE].success(data), wnd_value - nb))
                ) for (wnd_value, wnd_proba) in potential_wounds for nb in range(wnd_value+1)
            ]
            # unsaved += critic_wounds * self.unsaved_chances(
            #     armour, extra_rend=data.get(BONUS_REND, 0) + data.get(CRIT_BONUS_REND, 0))
            assert abs(sum([proba for (val, proba) in potential_unsaved]) - 1) <= pow(0.1, 5)

            # mortal_wounds += data.get(MW_ON_HIT_CRIT, 0) * critic_hits + data.get(MW_ON_WOUND_CRIT, 0) * critic_wounds
        except AssertionError:
            info = {
                'potential_attacks': potential_attacks,
                'potential_hits': potential_hits,
                'potential_wounds': potential_wounds,
                'potential_unsaved': potential_unsaved,
            }
            for k, potent in info.items():
                cleaned = [(
                    pick, round(sum([proba for (val, proba) in potent if val == pick]), 2)
                ) for pick in set([a for (a, b) in potent])]
                print(f' - {k}: {[(val, round(prob, 2))for (val, prob) in potent]}={cleaned}='
                      f'{sum([proba for (val, proba) in potent])} ({sum([proba for (val, proba) in potent]) - 1})')
            print(f'{int(100 * round(sum([proba for (damage, proba) in potential_unsaved if damage > 0]), 2))}% '
                  f'chances of damage')

        return sum([proba for (damage, proba) in potential_unsaved if damage > 0])


def binomial(n, k):
    # combinations of k in n
    return factorial(n) / (factorial(k) * factorial(n - k))
