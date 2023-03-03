from request import Request


class Packet:

    def __init__(self, requests: [Request], keep=False, one_time=False):
        self.requests = requests
        self.keep = keep
        self.one_time = one_time  # doc for one_time
