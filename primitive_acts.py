class PrimitiveAct:

    def __init__(self, object: str, act_from=None, act_to=None, container=None):
        self.object = [object]  # a container can contain >1 objects, or >1 parallel objects behave similarly
        self.act_from = act_from
        self.act_to = act_to
        self.container = container


class PSTOP(PrimitiveAct):
    pass


class PTRANS(PrimitiveAct):
    pass


class INGEST(PrimitiveAct):
    pass


class EXPEL(PrimitiveAct):
    pass


class STATECHANGE(PrimitiveAct):
    pass
