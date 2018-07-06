from typing import Tuple, List, Callable

from sigmar.basics.value import value


class Roll:
    def __init__(self, base_value):
        self.base_value = value(base_value)
        self.rerolls = 0
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod and reroll

    def chances(self, context: dict, mod=0) -> Tuple[float, float]:
        rerolls = self.rerolls
        for bonus in self.extra_bonuses:
            add_mod, add_reroll = bonus(context)
            mod += add_mod
            rerolls = max(rerolls, add_reroll)

        base_value = self.base_value.average(context) - mod
        chances = (7 - base_value) / 6
        rerolls_chance = 1 + min(rerolls, base_value - 1) / 6
        chances *= rerolls_chance
        sixes = rerolls_chance * max(0, 1 + mod) / 6 if base_value <= 6 else 0
        return max(0, chances - sixes), sixes

    def average(self, dices, context: dict, mod=0) -> Tuple[float, float]:
        chances, sixes = self.chances(context, mod)
        return chances * dices, sixes * dices
