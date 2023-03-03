from map import Containment, Space, Touching


class Frame:

    def __init__(self, containment: Containment, space: Space, touching: Touching):
        self.containment = containment
        self.space = space
        self.touching = touching
        self.actions = []
        self.actions_by_type = {"PTRANS": [], "PSTOP": [],
                                "INGEST": [], "EXPEL": [], "STATECHANGE": []}
        self.next = None
        self.empty = True  # only the initial state is empty
        self.sentence = None
