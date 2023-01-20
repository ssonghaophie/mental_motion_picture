class NounPhrase:

    def __init__(self, noun: str, combo=None):
        self.noun = noun
        self.combo = combo

    def __str__(self):
        res = self.noun
        if self.combo:
            res += "=(" + self.combo[0].noun
            for noun in self.combo[1:]:
                res += "+" + noun.noun
            res += ")"
        return res
