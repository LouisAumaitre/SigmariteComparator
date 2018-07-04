from typing import Tuple


class Roll:
    def __init__(self, base_value: int):
        self.base_value = base_value
        self.rerolls = 0

    def chances(self, mod=0) -> Tuple[float, float]:
        chances = (7 - self.base_value + mod) / 6
        rerolls = 1 + min(self.rerolls, self.base_value - 1) / 6
        chances *= rerolls
        sixes = rerolls * max(0, 1 + mod) / 6
        return chances, sixes

    def average(self, dices, mod=0) -> Tuple[float, float]:
        chances, sixes = self.chances(mod)
        return chances * dices, sixes * dices
