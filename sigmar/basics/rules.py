

class Rule:
    name: str = ""
    effect = None

    def __init__(self, name: str, effect):
        self.name = name
        self.effect = effect

    def apply(self, item):
        self.effect(item)
