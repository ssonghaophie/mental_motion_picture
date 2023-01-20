class PrimitiveAct:

    def __init__(self, obj: str, act_from=None, act_to=None, container=None):
        self.object = [obj]  # a container can contain >1 objects, or >1 parallel objects behave similarly
        self.act_from = act_from
        self.act_to = act_to
        self.container = container


class Pstop(PrimitiveAct):
    def __str__(self):
        res = "(objects: " + str(self.object)
        res += ")"
        return res


class Ptrans(PrimitiveAct):
    def __str__(self):
        res = "(objects: " + str(self.object)
        res += ", from: " + str(self.act_from)
        res += ", to: " + str(self.act_to)
        res += ")"
        return res


class Ingest(PrimitiveAct):
    def __str__(self):
        res = "(objects: " + str(self.object)
        res += ", container: " + str(self.container)
        res += ", from: " + str(self.act_from)
        res += ")"
        return res


class Expel(PrimitiveAct):
    def __str__(self):
        res = "(objects: " + str(self.object)
        res += ", container: " + str(self.container)
        res += ", to: " + str(self.act_to)
        res += ")"
        return res


class StateChange(PrimitiveAct):
    def __str__(self):
        res = "(objects: " + str(self.object)
        res += ", to: " + str(self.act_to)
        res += ")"
        return res
