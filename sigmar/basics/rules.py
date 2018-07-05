

class Rule:
    name: str = ""
    effect = None

    def __init__(self, name: str, effect):
        self.name = name
        self.effect = effect

    def apply(self, item):
        self.effect(item)


class Spell(Rule):
    def __init__(self, name, power, effect):
        Rule.__init__(self, name, effect)
        self.power = power

    def apply(self, item):
        try:
            item.spells.append(self)
        except Exception:
            raise ValueError(f'Spells must be given to units, not {item.__class__}')


class CommandAbility(Rule):
    def apply(self, item):
        try:
            item.command_abilities.append(self)
        except Exception:
            raise ValueError(f'Command Abilities must be given to units, not {item.__class__}')
