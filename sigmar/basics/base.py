from typing import Optional

import math


class Base:
    def __init__(self, depth: int, width: Optional[int]=None):
        self.depth = depth
        self.width = width if width is not None else depth

    def surface(self):
        return math.pi * self.width * self.width


infantry = Base(25)
large_infantry = Base(40)
cavalry = Base(50, 25)
monster = Base(60, 10)
