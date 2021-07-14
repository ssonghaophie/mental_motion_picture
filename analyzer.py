# Each word entry in the lexicon is a list of Request objects

class Request:

    def __init__(self, test=False, text=None, assign=None, next_packet=None):
        self.TEST = test
        self.TEST_TEXT = text
        self.ASSIGN = assign
        self.NEXT_PACKET = next_packet


# the ELI analyzer

class Analyzer:
    # Global variables
    part_of_speech = None
    CD = None

    def __init__(self, lexicon: {}):
        self.SENTENCE = []  # list of words
        self.STACK = []  # store word packets
        self.TRIGGERED = []  # triggered requests
        self.CD = None  # the output, what data structure?
        self.LEXICON = lexicon

        # read words from sentence
        self.length = 0  # length of the SENTENCE list
        self.pointer = 0  # index of the next word in SENTENCE

    def parse(self, sentence: str):
        """
        construct and run an analyzer

        @param sentence: input sentence
        @return:
        """
        self.split(sentence)

        # loop 1 - terminates when SENTENCE is empty
        while self.pointer < self.length:
            # read next word, put packet on top of stack
            self.STACK.append(self.read_word())

            # loop 2
            while self.STACK:
                trig_flag, trig_req = self.check_trig_req(self.STACK[-1])
                if trig_flag:
                    self.TRIGGERED.append(trig_req)
                    self.print_req(trig_req)
                    self.STACK.pop()
                    self.execute_req(trig_req)
                else:
                    break

            # loop 3
            while self.TRIGGERED:
                cur_request = self.TRIGGERED.pop()
                if cur_request.NEXT_PACKET:
                    self.STACK.append(cur_request.NEXT_PACKET)

        # if anything left on the stack, print it
        print("THE END..............................\n")
        print(len(self.STACK), "word packet(s) left on STACK:")
        for packet in self.STACK:
            print(" -", packet[0].TEST_TEXT)

    def split(self, sentence: str):
        """
        the input sentence is put into uppercase and split on all
        whitespace strings. The resulted list is appended on SENTENCE

        @param sentence: input sentence
        @return:
        """
        # remove leading and trailing characters and put into uppercase
        sentence = "*START* " + sentence.strip(".,?;:/\\ !@#$%^&*").upper()

        # split on whitespace characters
        split = sentence.split()
        self.SENTENCE.extend(split)
        self.length += len(split)

    def read_word(self) -> [Request]:
        """
        read the next word from self.SENTENCE, find the word in
        lexicon, and return the word packet

        @return:
        """
        word = self.SENTENCE[self.pointer]
        print("\nREAD WORD \"%s\"" % word)

        # check if the word has an entry in the lexicon
        if word in self.LEXICON:
            packet = self.LEXICON[word]
        else:
            print(word, "not found in lexicon!")
            return

        self.pointer += 1
        return packet

    @staticmethod
    def check_trig_req(packet: [Request]) -> (bool, Request):
        """
        check if there is a triggered Request in the packet. If yes, return the
        first triggered Request. If no, return an empty Request

        @param packet: word packet, a list of Requests
        @return: (boolean, Request)
        """
        for req in packet:
            if req.TEST:
                return True, req

        return False, Request()

    def execute_req(self, req: Request):
        """
        execute assignments in the Request

        @param req:
        @return:
        """
        Analyzer.print_exe(req)
        pass

    @staticmethod
    def print_req(request: Request):
        print(" - REQUEST TRIGGERED: \"%s\"" % request.TEST_TEXT)

    @staticmethod
    def print_exe(request: Request):
        pass
