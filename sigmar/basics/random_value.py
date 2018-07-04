from typing import Union, List, Callable


class RandomValue:
    defined_value: Union[str, int] = 0

    def __init__(self, defined_value: Union[str, int]):
        self.defined_value = defined_value
        self.extra_bonuses: List[Callable] = []  # function take dict, return mod and extra_ignore

    def average(self, extra_data: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(extra_data)
            mod += add_mod

        if isinstance(self.defined_value, int):
            return self.defined_value + mod
        elif self.defined_value == 'D6':
            return 3.5 + mod
        else:
            return 0 + mod

    def max(self, extra_data: dict, mod=0):
        for bonus in self.extra_bonuses:
            add_mod, extra_ignore = bonus(extra_data)
            mod += add_mod

        if isinstance(self.defined_value, int):
            return self.defined_value + mod
        elif self.defined_value == 'D6':
            return 6 + mod
        else:
            return 0 + mod


def rv(defined_value: Union[str, int, RandomValue]):
    if isinstance(defined_value, RandomValue):
        return defined_value
    return RandomValue(defined_value)
