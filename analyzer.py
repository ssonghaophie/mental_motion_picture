# Each word entry in the lexicon is a list of requests

class Request:

    def __init__(self, test=None, assign=None, next_packet=None):
        self.TEST = test
        self.ASSIGN = assign
        self.NEXT_PACKET = next_packet


# the ELI analyzer

class Analyzer:

    def __init__(self):
        self.SENTENCE = []  # list or linked list?
        self.STACK = []  # store word packets
        self.TRIGGERED_REQUESTS = []
        self.CD = None  # the output, what data structure?

    def parse(self, sentence):
        """take input from user and add to self.SENTENCE

        Args:
            sentencce (string): input sentence
        """
        pass

    def next_word(self):
        """read the next word from self.SENTENCE, find the word in 
        lexicon, and load the word packet to stack
        """
        pass

    def get_top_packet(self):
        pass

    def remove_packet(self):
        pass
