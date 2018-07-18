from typing import List, Callable

from copy import copy

from sigmar.basics.roll import Roll
from sigmar.basics.value import Value
from sigmar.basics.weapon import binomial


def attack_round(
            attacks: Value,
            tohit: Roll,
            towound: Roll,
            rend: Value,
            damage: Value,
            rules: List[Callable],
            context: dict,
            users=1,
):
    my_context = copy(context)
    for r in rules:
        r(my_context)

    potential_attacks = {}
    potential_hits = {}
    potential_wounds = {}
    potential_unsaved = {}
    try:
        potential_attacks = [(nb * users, proba) for (nb, proba) in attacks.potential_values(context)]
        assert abs(sum([proba for (val, proba) in potential_attacks]) - 1) <= pow(0.1, 5)
        potential_attacks = [
            (pick, round(sum([
                proba for (val, proba) in potential_attacks if val == pick
            ]), 2)) for pick in set([a for (a, b) in potential_attacks])
        ]

        # potential_hits = [
        #     (
        #         nb, atk_proba * binomial(atk_value, nb) * (pow(self.tohit.success(data), nb) * pow(
        #             self.tohit.fail(data), atk_value - nb))
        #     ) for (atk_value, atk_proba) in potential_attacks for nb in range(atk_value + 1)
        # ]
        # # hits = hits + critic_hits * data.get(EXTRA_HIT_ON_CRIT, 0)
        # assert abs(sum([proba for (val, proba) in potential_hits]) - 1) <= pow(0.1, 5)
        #
        # potential_wounds = [
        #     (
        #         nb, hit_proba * binomial(hit_value, nb) * (pow(self.towound.success(data), nb) * pow(
        #             self.towound.fail(data), hit_value - nb))
        #     ) for (hit_value, hit_proba) in potential_hits for nb in range(hit_value + 1)
        # ]
        # # _wounds, _critic_wounds = self.average_wounds(critic_hits, data, mod=data.get(TOWOUND_MOD_ON_CRIT_HIT, 0))
        # # wounds += critic_wounds * data.get(EXTRA_WOUND_ON_CRIT, 0)
        # assert abs(sum([proba for (val, proba) in potential_wounds]) - 1) <= pow(0.1, 5)
        #
        # potential_unsaved = [
        #     (
        #         nb, wnd_proba * binomial(wnd_value, nb) * (pow(data[ENEMY_SAVE].fail(data), nb) * pow(
        #             data[ENEMY_SAVE].success(data), wnd_value - nb))
        #     ) for (wnd_value, wnd_proba) in potential_wounds for nb in range(wnd_value + 1)
        # ]
        # # unsaved += critic_wounds * self.unsaved_chances(
        # #     armour, extra_rend=data.get(BONUS_REND, 0) + data.get(CRIT_BONUS_REND, 0))
        # assert abs(sum([proba for (val, proba) in potential_unsaved]) - 1) <= pow(0.1, 5)

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

    return {
            'potential_attacks': potential_attacks,
            'potential_hits': potential_hits,
            'potential_wounds': potential_wounds,
            'potential_unsaved': potential_unsaved,
        }