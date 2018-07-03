from typing import Union


class RandomValue:
    defined_value: Union[str, int] = 0

    def __init__(self, defined_value: Union[str, int]):
        self.defined_value = defined_value

    def average(self):
        if isinstance(self.defined_value, int):
            return self.defined_value
        elif self.defined_value == 'D6':
            return 3.5
        else:
            return 0

    def max(self):
        if isinstance(self.defined_value, int):
            return self.defined_value
        elif self.defined_value == 'D6':
            return 6
        else:
            return 0


def rv(defined_value: Union[str, int, RandomValue]):
    if isinstance(defined_value, RandomValue):
        return defined_value
    return RandomValue(defined_value)
