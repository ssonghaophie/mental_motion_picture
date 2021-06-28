# Each word entry in the lexicon is a list of Request obecjects

class Request:

    def __init__(self, test=False, assign=None, next_packet=None):
        self.TEST = test
        self.ASSIGN = assign
        self.NEXT_PACKET = next_packet


# the ELI analyzer

class Analyzer:

    # Global variables
    part_of_speech = None
    CD = None

    def __init__(self, lexicon):
        self.SENTENCE = []  # list of words
        self.STACK = []  # store word packets
        self.TRIGGERED = []  # triggered requests
        self.CD = None  # the output, what data structure?
        self.lexicon = lexicon

        self.length = 0  # length of the SENTENCE list
        self.pointer = 0  # index of the next word in SENTENCE

    def parse(self, sentence):
        self.split(sentence)
        self.read_word()
        top_packet = self.get_top_packet()
        return top_packet

        # enter loop

    def split(self, sentence):
        """the input sentence is put into uppercase and split on all
        whitespace strings. The resulted list is appended on SENTENCE

        Args:
            sentencce (string): input sentence
        """
        # remove leading and trailing characters and put into uppercase
        sentence = sentence.strip(".,?!;:/\\ ").upper()
        # split on whitespace characters
        split = sentence.split()
        self.SENTENCE.extend(split)
        self.length += len(split)

    def read_word(self):
        """read the next word from self.SENTENCE, find the word in 
        lexicon, and load the word packet to stack
        """
        word = self.SENTENCE[self.pointer]

        # check if the word has an entry in the lexicon
        if word in self.lexicon:
            packet = self.lexicon[word]
        else:
            print(word, "not found in lexicon!")
            return

        self.STACK.append(packet)
        self.pointer += 1

    def get_top_packet(self):
        return self.STACK.pop()

    # def remove_packet(self):
    #     pass
