from typing import Tuple, List, Callable


class Roll:
    def __init__(self, base_value: int):
        self.base_value = base_value
        self.rerolls = 0
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod and reroll

    def chances(self, context: dict, mod=0) -> Tuple[float, float]:
        rerolls = self.rerolls
        for bonus in self.extra_bonuses:
            add_mod, add_reroll = bonus(context)
            mod += add_mod
            rerolls = max(rerolls, add_reroll)

        chances = (7 - self.base_value + mod) / 6
        rerolls_chance = 1 + min(rerolls, self.base_value - 1) / 6
        chances *= rerolls_chance
        sixes = rerolls_chance * max(0, 1 + mod) / 6
        return chances - sixes, sixes

    def average(self, dices, context: dict, mod=0) -> Tuple[float, float]:
        chances, sixes = self.chances(context, mod)
        return chances * dices, sixes * dices
