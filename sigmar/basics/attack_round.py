from typing import List, Callable
from copy import copy
from math import factorial

from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import (
    ENEMY_SAVE, EXTRA_HIT_ON_CRIT, EXTRA_DAMAGE_ON_CRIT_WOUND,
    EXTRA_ATTACK_ON_HIT, TOWOUND_MOD_ON_CRIT_HIT, MW_ON_HIT_CRIT,
    MW_ON_WOUND_CRIT, CRIT_BONUS_REND, EXTRA_WOUND_ON_CRIT,
    AUTO_WOUND_ON_CRIT, MW_ON_DAMAGE, MW_IF_DAMAGE)
from sigmar.basics.value import Value, value


def binomial(n, k):
    # combinations of k in n
    return factorial(n) / (factorial(k) * factorial(n - k))


def probability_of_hit_and_crit(dices, success, crit, roll: Roll, context) -> float:
    success_rate = binomial(dices, success)
    success_rate *= pow(roll.success(context), success) * pow(roll.fail(context), dices - success)
    crit_rate = binomial(success, crit) * pow(
        roll.critic_given_success(context), crit
    ) * pow(roll.no_critic_given_success(context), success - crit)
    return success_rate * crit_rate


def probability_of_wound_and_crit(dices, success, crit, roll: Roll, context, crit_hit=0) -> float:
    succ_crit_hit = min(crit_hit, success)
    failed_crit_hit = crit_hit - succ_crit_hit
    if context.get(AUTO_WOUND_ON_CRIT, False) and (failed_crit_hit or crit > success - succ_crit_hit):
        # cannot fail, nor get a critical wound roll an automatic success
        return 0
    success_rate = binomial(dices, success)
    # successful after a critical_hit
    if not context.get(AUTO_WOUND_ON_CRIT, False):
        success_rate *= pow(roll.success(context, context.get(TOWOUND_MOD_ON_CRIT_HIT, 0)), succ_crit_hit)
    # successful without a critical_hit
    success_rate *= pow(roll.success(context), success - succ_crit_hit)
    # failed despite a critical_hit
    success_rate *= pow(roll.fail(context, context.get(TOWOUND_MOD_ON_CRIT_HIT, 0)), failed_crit_hit)
    # failed without a critical_hit
    success_rate *= pow(roll.fail(context), dices - success - failed_crit_hit)

    # crit rate may be flawed in case of crit_hit bonuses TODO: fix
    crit_rate = binomial(success, crit)
    # critical wound after a critical_hit
    crit_rate *= pow(roll.critic_given_success(context), crit)
    if not (context.get(AUTO_WOUND_ON_CRIT, False) and crit_hit):
        crit_rate *= pow(roll.no_critic_given_success(context), success - crit)
    return success_rate * crit_rate


def probability_of_save_fail(dices, success, roll: Roll, context, rend, crit_wnd=0) -> float:
    pass_rate = binomial(dices, success)
    pass_rate *= pow(roll.fail(context, rend + context.get(CRIT_BONUS_REND, 0)), crit_wnd)
    pass_rate *= pow(roll.fail(context, rend), success - crit_wnd)
    pass_rate *= pow(roll.success(context, rend), dices - success)
    return pass_rate


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
    potential_damage = {}
    cleaned_damage = []
    try:
        potential_attacks = [{
            'attacks': nb * users, 'proba': proba,
        } for (nb, proba) in attacks.potential_values(my_context)]
        assert abs(sum([att['proba'] for att in potential_attacks]) - 1) <= pow(0.1, 5)
        potential_attacks = [{
            'mortal_wounds': value(0),
            'attacks': pick,
            'proba': sum([att['proba'] for att in potential_attacks if att['attacks'] == pick])
        } for pick in set(att['attacks'] for att in potential_attacks)]

        potential_hits = [
            {
                **att,
                'hits': value(nb) + my_context.get(EXTRA_HIT_ON_CRIT, 0) * nb_crit,
                'crit_hits': nb_crit,
                'second_attacks': nb * my_context.get(EXTRA_ATTACK_ON_HIT, 0),
                'proba': att['proba'] * probability_of_hit_and_crit(att['attacks'], nb, nb_crit, tohit, my_context)
            } for att in potential_attacks for nb in range(att['attacks'] + 1) for nb_crit in range(nb + 1)
        ]
        potential_hits = [
            {
                **att,
                'hits': att['hits'] + value(nb) + my_context.get(EXTRA_HIT_ON_CRIT, 0) * nb_crit,
                'crit_hits': nb_crit + att['crit_hits'],
                'proba': att['proba'] * probability_of_hit_and_crit(
                    att['second_attacks'], nb, nb_crit, tohit, my_context)
            } for att in potential_hits for nb in range(att['second_attacks'] + 1) for nb_crit in range(nb + 1)
        ]
        potential_hits = [
            {
                **hit,
                'hits': nb,
                'mortal_wounds': hit['mortal_wounds'] + my_context.get(MW_ON_HIT_CRIT, 0) * hit['crit_hits'],
                'proba': hit['proba'] * proba,
            } for hit in potential_hits for (nb, proba) in hit['hits'].potential_values(my_context)
        ]
        assert abs(sum([hit['proba'] for hit in potential_hits]) - 1) <= pow(0.1, 5)

        potential_wounds = [
            {
                **hit,
                'wounds': value(nb) + my_context.get(EXTRA_WOUND_ON_CRIT, 0) * nb_crit,
                'crit_wounds': nb_crit,
                'mortal_wounds': hit['mortal_wounds'] + my_context.get(MW_ON_WOUND_CRIT, 0) * nb_crit,
                'proba': hit['proba'] * probability_of_wound_and_crit(
                    hit['hits'], nb, nb_crit, towound, my_context, crit_hit=hit['crit_hits'])
            } for hit in potential_hits for nb in range(hit['hits'] + 1) for nb_crit in range(nb + 1)
        ]
        potential_wounds = [
            {
                **wnd,
                'wounds': nb,
                'proba': wnd['proba'] * proba,
            } for wnd in potential_wounds for (nb, proba) in wnd['wounds'].potential_values(my_context)
        ]
        assert abs(sum([wnd['proba'] for wnd in potential_wounds]) - 1) <= pow(0.1, 5)

        potential_unsaved = [
            {
                **wnd,
                'unsaved': nb,
                'proba': wnd['proba'] * probability_of_save_fail(
                    wnd['wounds'],
                    nb, my_context[ENEMY_SAVE],
                    my_context,
                    rend=rend.average(my_context),
                    crit_wnd=wnd['crit_wounds'])
            } for wnd in potential_wounds for nb in range(wnd['wounds'] + 1)
        ]
        assert abs(sum([unsvd['proba'] for unsvd in potential_unsaved]) - 1) <= pow(0.1, 5)

        potential_damage = []
        for unsvd in potential_unsaved:
            potential_results = {0: 1}
            for att in range(unsvd['unsaved']):
                new_results = {}
                for (val, val_proba) in damage.potential_values(my_context):
                    for total, total_proba in potential_results.items():
                        new_results[total + val] = val_proba * total_proba + new_results.get(total + val, 0)
                potential_results = new_results
            potential_results = [(k, v) for k, v in potential_results.items()]

            potential_damage.extend([
                {
                    **unsvd,
                    'damage': nb + unsvd['crit_wounds'] * my_context.get(EXTRA_DAMAGE_ON_CRIT_WOUND, 0),
                    'mortal_wounds': unsvd['mortal_wounds'] + (
                        my_context.get(MW_ON_DAMAGE, 0) * nb) + (
                        my_context.get(MW_IF_DAMAGE, 0) if nb else 0),
                    'proba': unsvd['proba'] * proba,
                } for (nb, proba) in potential_results
            ])

        potential_full_damage = [
            {
                **dmg,
                'damage': dmg['damage'] + nb,
                'mortal_wounds': nb,
                'proba': dmg['proba'] * proba,
            } for dmg in potential_damage for (nb, proba) in dmg['mortal_wounds'].potential_values(my_context)
        ]

        cleaned_damage = [{
            'damage': pick * (1 + context.get(MW_ON_DAMAGE, 0)),
            'proba': sum([dmg['proba'] for dmg in potential_full_damage if dmg['damage'] == pick])
        } for pick in set(dmg['damage'] for dmg in potential_full_damage)]
    except AssertionError:
        info = {
            'potential_attacks': potential_attacks,
            'potential_hits': potential_hits,
            'potential_wounds': potential_wounds,
            'potential_unsaved': potential_unsaved,
            'potential_damage': potential_damage,
            'cleaned_damage': cleaned_damage,
        }
        for k, potent in info.items():
            print(f'- {k}:')
            for e in potent:
                print(str({k: str(v) for k, v in e.items()}).replace("'", "").replace("\"", ""))
            sum_proba = sum(e['proba'] for e in potent)
            print(f'   total={sum_proba}')

    return cleaned_damage


def average_damage_computer(
            attacks: Value,
            tohit: Roll,
            towound: Roll,
            rend: Value,
            damage: Value,
            rules: List[Callable],
            context: dict,
            users=1,
) -> float:
    dmg = attack_round(attacks, tohit, towound, rend, damage, rules, context, users)
    return sum([e['damage'] * e['proba'] for e in dmg])
