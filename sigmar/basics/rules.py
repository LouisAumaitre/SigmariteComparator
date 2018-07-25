

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


ARCANE_BOLT = Spell('Arcane Bolt', 5, None)
MAGIC_SHIELD = Spell('Magic Shield', 5, None)


class CommandAbility(Rule):
    def apply(self, item):
        try:
            item.command_abilities.append(self)
        except Exception:
            raise ValueError(f'Command Abilities must be given to units, not {item.__class__}')


class CommentRule(Rule):
    def __init__(self, name, comment):
        Rule.__init__(self, name, None)
        self.comment = comment

    def apply(self, item):
        item.notes.append(self.comment)


class TodoRule(Rule):
    def __init__(self, name):
        Rule.__init__(self, name, None)

    def apply(self, item):
        item.notes.append(self.name)
        # print(f'Remember to do rule {self.name} for item {item.name}')
