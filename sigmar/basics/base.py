from typing import Optional

import math


class Base:
    def __init__(self, depth: int, width: Optional[int]=None):
        self.depth = depth
        self.width = width if width is not None else depth

    def surface(self):
        return math.pi * self.width * self.width


infantry_base = Base(25)
large_infantry_base = Base(40)
cavalry_base = Base(50, 25)
monster_base = Base(60, 10)
