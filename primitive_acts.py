class Acts:

    def __init__(self, object: str, act_from=None, act_to=None, container=None):
        self.object = [object]  # a container can contain >1 objects, or >1 parallel objects behave similarly
        self.act_from = act_from
        self.act_to = act_to
        self.container = container


class PSTOP(Acts):
    pass


class PTRANS(Acts):
    pass


class INGEST(Acts):
    pass


class EXPEL(Acts):
    pass


class STATECHANGE(Acts):
    pass
