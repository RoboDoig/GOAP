class Action:
    def __init__(self, name, preconditions, effects, repeatable, cost=1):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.repeatable = repeatable
        self.cost = cost

    def check_procedural(self):
        return True
