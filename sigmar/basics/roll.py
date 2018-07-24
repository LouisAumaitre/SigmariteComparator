from typing import Tuple, List, Callable

from sigmar.basics.value import value, FixedValue


class Roll:
    def __init__(self, base_value) -> None:
        if isinstance(base_value, Roll):
            self.base_value = base_value.base_value
        else:
            self.base_value = value(base_value)
        self.rerolled = 0
        self.rules: List[Callable] = []  # function take dict, return mod and reroll
        self.mod_ignored = []

    def chances(self, context: dict, mod=0) -> Tuple[float, float]:
        if isinstance(self.base_value, FixedValue) and self.base_value.defined_value == 1:
            return 1, 0
        rerolled = self.rerolled
        if mod in self.mod_ignored or 'all' in self.mod_ignored:
            mod = 0

        for bonus in self.rules:
            add_mod, add_reroll = bonus(context)
            mod += add_mod
            rerolled = max(rerolled, add_reroll)

        base_value = self.base_value.average(context) - mod
        chances = (7 - base_value) / 6
        rerolls_chance = 1 + min(rerolled, base_value - 1) / 6
        chances *= rerolls_chance
        sixes = rerolls_chance * max(0, 1 + mod) / 6 if base_value <= 6 else 0
        return max(0, chances - sixes), sixes

    def success(self, context: dict, mod=0):
        hit, crit = self.chances(context, mod)
        return hit + crit

    def fail(self, context: dict, mod=0):
        hit, crit = self.chances(context, mod)
        return 1 - hit - crit

    def critic_given_success(self, context: dict, mod=0):
        hit, crit = self.chances(context, mod)
        if hit + crit == 0:
            return 0
        return crit / (hit + crit)

    def no_critic_given_success(self, context: dict, mod=0):
        hit, crit = self.chances(context, mod)
        if hit + crit == 0:
            return 1
        return 1 - (crit / (hit + crit))

    def average(self, dices, context: dict, mod=0) -> Tuple[float, float]:
        chances, sixes = self.chances(context, mod)
        return chances * dices, sixes * dices

    def __str__(self):
        return f'roll_{self.base_value}+'
