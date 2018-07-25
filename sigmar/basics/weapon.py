from typing import List, Union, Tuple, Callable, Dict
from math import factorial
from copy import copy

from sigmar.basics.value import Value, value
from sigmar.basics.roll import Roll
from sigmar.basics.rules import Rule
from sigmar.basics.string_constants import (
    WEAPON_RANGE,
    RANGE,
    ENEMY_SAVE,
    AUTO_WOUND_ON_CRIT, CRIT_BONUS_REND, TOWOUND_MOD_ON_CRIT_HIT, EXTRA_HIT_ON_CRIT, EXTRA_ATTACK_ON_HIT,
    EXTRA_WOUND_ON_CRIT, MW_ON_WOUND_CRIT, MW_ON_HIT_CRIT, MW_ON_DAMAGE, MW_IF_DAMAGE, EXTRA_DAMAGE_ON_CRIT_WOUND,
    NUMBER_OF_HITS, MORTAL_WOUNDS, MORTAL_WOUNDS_PER_ATTACK)


class Weapon:
    def __init__(
            self,
            name: str,
            range_: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            attacks: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            tohit,
            towound,
            rend,
            damage: Union[int, str, Value, Dict[int, Union[int, str, Value]]],
            rules: List[Rule],
    ) -> None:
        self.name = name
        self.range = value(range_)
        self.attacks = value(attacks)
        self.tohit = Roll(tohit)
        self.towound = Roll(towound)
        self.rend = value(rend)
        self.damage = value(damage)

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

    def average_damage(self, context: dict, users=1):
        if context.get(RANGE, 0) > self.range.average(context) or \
                                self.range.average(context) > 3 >= context.get(RANGE, 0):
            return 0
        context[WEAPON_RANGE] = self.range.average(context)
        dmg = self.attack_round(copy(context), users)
        return sum([e['damage'] * e['proba'] for e in dmg])

    def attack_round(self, context, users=1):
        my_context = copy(context)
        for r in self.attack_rules:
            r(my_context)

        potential_attacks = {}
        potential_hits = {}
        potential_wounds = {}
        potential_unsaved = {}
        potential_damage = {}
        cleaned_damage = []
        try:
            potential_attacks = [{
                'attacks': nb * users,
                'proba': proba,
                'mortal_wounds': my_context.get(
                    MORTAL_WOUNDS, value(0)) + my_context.get(MORTAL_WOUNDS_PER_ATTACK, 0) * nb * users,
            } for (nb, proba) in self.attacks.potential_values(my_context)]
            assert abs(sum([att['proba'] for att in potential_attacks]) - 1) <= pow(0.1, 5)
            potential_attacks = cleaned_dict_list(potential_attacks, ['attacks', 'mortal_wounds'])

            potential_hits = compute_potential_hits(my_context, potential_attacks, self.tohit)
            assert abs(sum([hit['proba'] for hit in potential_hits]) - 1) <= pow(0.1, 5)
            potential_hits = cleaned_dict_list(potential_hits, ['hits', 'crit_hits', 'mortal_wounds'])

            potential_wounds = compute_potential_wounds(my_context, potential_hits, self.towound)
            assert abs(sum([wnd['proba'] for wnd in potential_wounds]) - 1) <= pow(0.1, 5)
            potential_wounds = cleaned_dict_list(potential_wounds, ['wounds', 'crit_wounds', 'mortal_wounds'])

            potential_unsaved = [
                {
                    **wnd,
                    'unsaved': nb,
                    'unsaved_crit_wound': nb_crit,
                    'proba': wnd['proba'] * probability_of_save_fail(
                        wnd['wounds'],
                        nb, nb_crit, my_context[ENEMY_SAVE],
                        my_context,
                        rend=self.rend.average(my_context),
                        crit_wnd=wnd['crit_wounds'])
                } for wnd in potential_wounds
                for nb in range(wnd['wounds'] + 1)
                for nb_crit in range(max(0, wnd['crit_wounds'] - (wnd['wounds'] - nb)), min(wnd['crit_wounds'], nb) + 1)
            ]
            assert abs(sum([unsvd['proba'] for unsvd in potential_unsaved]) - 1) <= pow(0.1, 5)
            potential_unsaved = cleaned_dict_list(potential_unsaved, ['unsaved', 'unsaved_crit_wound', 'mortal_wounds'])

            potential_damage = compute_potential_damage(self.damage, my_context, potential_unsaved)
            assert abs(sum([dmg['proba'] for dmg in potential_damage]) - 1) <= pow(0.1, 5)

            potential_full_damage = [
                {
                    **dmg,
                    'damage': dmg['damage'] + nb,
                    'mortal_wounds': nb,
                    'proba': dmg['proba'] * proba,
                } for dmg in potential_damage for (nb, proba) in dmg['mortal_wounds'].potential_values(my_context)
            ]
            potential_full_damage = cleaned_dict_list(potential_full_damage, ['damage'])

            cleaned_damage = [{
                'damage': pick * (1 + context.get(MW_ON_DAMAGE, 0)),
                'proba': sum([dmg['proba'] for dmg in potential_full_damage if dmg['damage'] == pick])
            } for pick in set(dmg['damage'] for dmg in potential_full_damage)]
            # raise AssertionError  # testing
        except AssertionError:
            info = {
                'potential_attacks': potential_attacks,
                'potential_hits': potential_hits,
                'potential_wounds': potential_wounds,
                'potential_unsaved': potential_unsaved,
                'potential_damage': potential_damage,
                'cleaned_damage': cleaned_damage,
            }
            print(self.name)
            for k, potent in info.items():
                print(f'- {k}:')
                for e in potent:
                    print(str({k: str(v) for k, v in e.items()}).replace("'", "").replace("\"", ""))
                sum_proba = sum(e['proba'] for e in potent)
                print(f'   total={sum_proba}')
            average = sum(d.get('damage') * d.get('proba') for d in cleaned_damage)
            print(f'AVERAGE: {average}')

        return cleaned_damage


def cleaned_dict_list(list_of_dicts, keys_to_keep):
    new_list = []
    for d in list_of_dicts:
        ok = False
        for already_in in new_list:
            if len([k for k in keys_to_keep if d[k] == already_in[k]]) == len(keys_to_keep):  # keys are good
                already_in['proba'] += d['proba']
                ok = True
                break
        if not ok:
            new_list.append({k: d[k] for k in [*keys_to_keep, 'proba']})
    return new_list


def compute_potential_damage(damage, context, potential_unsaved):
    potential_damage = []
    for unsvd in potential_unsaved:
        potential_results = {0: 1}
        crit_damage = damage + context.get(EXTRA_DAMAGE_ON_CRIT_WOUND, 0)
        for att in range(min(unsvd['unsaved'], unsvd['unsaved_crit_wound'])):
            new_results = {}
            for (val, val_proba) in crit_damage.potential_values(context):
                for total, total_proba in potential_results.items():
                    new_results[total + val] = val_proba * total_proba + new_results.get(total + val, 0)
            potential_results = new_results
        for att in range(max(unsvd['unsaved'] - unsvd['unsaved_crit_wound'], 0)):
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
                'mortal_wounds': unsvd['mortal_wounds'] + (
                    context.get(MW_ON_DAMAGE, 0) * nb) + (context.get(MW_IF_DAMAGE, 0) if nb else 0),
                'proba': unsvd['proba'] * proba,
            } for (nb, proba) in potential_results
        ])
    return potential_damage


def compute_potential_wounds(context, potential_hits, towound):
    potential_wounds = [
        {
            **hit,
            'wounds': value(nb) + context.get(EXTRA_WOUND_ON_CRIT, 0) * nb_crit,
            'crit_wounds': nb_crit,
            'mortal_wounds': hit['mortal_wounds'] + context.get(MW_ON_WOUND_CRIT, 0) * nb_crit,
            'proba': hit['proba'] * probability_of_wound_and_crit(
                hit['hits'], nb, nb_crit, towound, context, crit_hit=hit['crit_hits'])
        } for hit in potential_hits for nb in range(hit['hits'] + 1) for nb_crit in range(nb + 1)
    ]
    potential_wounds = [
        {
            **wnd,
            'wounds': nb,
            'proba': wnd['proba'] * proba,
        } for wnd in potential_wounds for (nb, proba) in wnd['wounds'].potential_values(context)
    ]
    return potential_wounds


def compute_potential_hits(context, potential_attacks, tohit):
    potential_hits = [
        {
            **att,
            'hits': value(nb) * context.get(NUMBER_OF_HITS, 1) + context.get(EXTRA_HIT_ON_CRIT, 0) * nb_crit,
            'crit_hits': nb_crit,
            'second_attacks': nb * context.get(EXTRA_ATTACK_ON_HIT, 0),
            'proba': att['proba'] * probability_of_hit_and_crit(att['attacks'], nb, nb_crit, tohit, context)
        } for att in potential_attacks for nb in range(att['attacks'] + 1) for nb_crit in range(nb + 1)
    ]
    potential_hits = [
        {
            **att,
            'hits': att['hits'] + value(nb) + context.get(EXTRA_HIT_ON_CRIT, 0) * nb_crit,
            'crit_hits': nb_crit + att['crit_hits'],
            'proba': att['proba'] * probability_of_hit_and_crit(
                att['second_attacks'], nb, nb_crit, tohit, context)
        } for att in potential_hits for nb in range(att['second_attacks'] + 1) for nb_crit in range(nb + 1)
    ]
    potential_hits = [
        {
            **hit,
            'hits': nb,
            'mortal_wounds': hit['mortal_wounds'] + context.get(MW_ON_HIT_CRIT, 0) * hit['crit_hits'],
            'proba': hit['proba'] * proba,
        } for hit in potential_hits for (nb, proba) in hit['hits'].potential_values(context)
    ]
    return potential_hits


def binomial(n, k):
    # combinations of k in n
    if k > n:
        raise ValueError(f'binomial of {k} in {n}')
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


def probability_of_save_fail(dices, success, after_crit_wound, roll: Roll, context, rend, crit_wnd=0) -> float:
    if after_crit_wound > success:
        raise ValueError(f'trying to compute {after_crit_wound} success after crit amongst {success} successes')
    if after_crit_wound > crit_wnd:
        raise ValueError(f'trying to compute {after_crit_wound} success after crit with {crit_wnd} crits')

    regular_pass_rate = binomial(dices - crit_wnd, success - after_crit_wound)
    regular_pass_rate *= pow(roll.fail(context, rend), success - after_crit_wound)
    regular_pass_rate *= pow(roll.success(context, rend), (dices - crit_wnd) - (success - after_crit_wound))

    crit_pass_rate = binomial(crit_wnd, after_crit_wound)
    crit_pass_rate *= pow(roll.fail(context, rend + context.get(CRIT_BONUS_REND, 0)), after_crit_wound)
    crit_pass_rate *= pow(roll.success(context, rend + context.get(CRIT_BONUS_REND, 0)), crit_wnd - after_crit_wound)

    return regular_pass_rate * crit_pass_rate
