from typing import List, Callable
from copy import copy
from math import factorial

from sigmar.basics.roll import Roll
from sigmar.basics.string_constants import ENEMY_SAVE
from sigmar.basics.value import Value


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


def probability_of_wound_and_crit(dices, success, crit, roll: Roll, context) -> float:
    success_rate = binomial(dices, success)
    success_rate *= pow(roll.success(context), success) * pow(roll.fail(context), dices - success)
    crit_rate = binomial(success, crit) * pow(
        roll.critic_given_success(context), crit
    ) * pow(roll.no_critic_given_success(context), success - crit)
    return success_rate * crit_rate


def probability_of_save_fail(dices, success, roll: Roll, context, rend) -> float:
    pass_rate = binomial(dices, success)
    pass_rate *= pow(roll.fail(context, rend), success) * pow(roll.success(context, rend), dices - success)
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
    cleaned_damage = []
    try:
        potential_attacks = [{
            'attacks': nb * users, 'proba': proba
        } for (nb, proba) in attacks.potential_values(context)]
        assert abs(sum([att['proba'] for att in potential_attacks]) - 1) <= pow(0.1, 5)
        potential_attacks = [{
            'attacks': pick,
            'proba': sum([att['proba'] for att in potential_attacks if att['attacks'] == pick])
        } for pick in set(att['attacks'] for att in potential_attacks)]

        try:
            potential_hits = [
                {
                    **att,
                    'hits': nb,
                    'crit_hits': nb_crit,
                    'proba': att['proba'] * probability_of_hit_and_crit(att['attacks'], nb, nb_crit, tohit, context)
                } for att in potential_attacks for nb in range(att['attacks'] + 1) for nb_crit in range(nb + 1)
            ]
        except TypeError as e:
            print(f'{attacks}=>{potential_attacks}')
            raise e
        assert abs(sum([hit['proba'] for hit in potential_hits]) - 1) <= pow(0.1, 5)

        potential_wounds = [
            {
                **hit,
                'wounds': nb,
                'crit_wounds': nb_crit,
                'proba': hit['proba'] * probability_of_wound_and_crit(hit['hits'], nb, nb_crit, towound, context)
            } for hit in potential_hits for nb in range(hit['hits'] + 1) for nb_crit in range(nb + 1)
        ]
        assert abs(sum([wnd['proba'] for wnd in potential_wounds]) - 1) <= pow(0.1, 5)

        potential_unsaved = [
            {
                **wnd,
                'unsaved': nb,
                'proba': wnd['proba'] * probability_of_save_fail(
                    wnd['wounds'], nb, context[ENEMY_SAVE], context, rend=rend.average(context))
            } for wnd in potential_wounds for nb in range(wnd['wounds'] + 1)
        ]
        assert abs(sum([unsvd['proba'] for unsvd in potential_unsaved]) - 1) <= pow(0.1, 5)

        potential_damage = []
        for unsvd in potential_unsaved:
            potential_results = {0: 1}
            for att in range(unsvd['unsaved']):
                new_results = {}
                for (val, val_proba) in damage.potential_values(context):
                    for total, total_proba in potential_results.items():
                        new_results[total + val] = val_proba * total_proba + new_results.get(total + val, 0)
                potential_results = new_results
            potential_results = [(k, v) for k, v in potential_results.items()]

            potential_damage.extend([
                {
                    **unsvd,
                    'damage': nb,
                    'proba': unsvd['proba'] * proba
                } for (nb, proba) in potential_results
            ])

        cleaned_damage = [{
            'damage': pick,
            'proba': sum([dmg['proba'] for dmg in potential_damage if dmg['damage'] == pick])
        } for pick in set(dmg['damage'] for dmg in potential_damage)]
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