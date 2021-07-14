# Each word entry in the lexicon is a list of Request objects
class Request:

    def __init__(self, text=None, test=False, test_val=None, assign_val=None, next_packet=None):
        self.TEXT = text  # short explanation of the Request
        self.TEST = test  # boolean
        self.TEST_VAL = test_val  # if all evaluations pass, set test to be True
        self.ASSIGN_VAL = assign_val  # assignments to complete if test==True
        self.NEXT_PACKET = next_packet


# the ELI analyzer
class Analyzer:
    val = {"CD": None, "part-of-speech": None}

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
                    self.STACK.pop()
                    if trig_req.ASSIGN_VAL:
                        self.execute_assign(trig_req)
                else:
                    break

            # loop 3
            while self.TRIGGERED:
                cur_request = self.TRIGGERED.pop()
                if cur_request.NEXT_PACKET:
                    self.STACK.append(cur_request.NEXT_PACKET)

        # if anything left on the stack, print it
        print("\n________________________________________________________")
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print("|||||||||||||||||||||| THE END |||||||||||||||||||||||||")
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n")
        print(len(self.STACK), "word packet(s) left on STACK:")
        for packet in self.STACK:
            print(" -", packet[0].TEXT)

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
        print("--------------------------------------------------------")
        print("READ WORD \"%s\"" % word)

        # check if the word has an entry in the lexicon
        if word in self.LEXICON:
            packet = self.LEXICON[word]
        else:
            print(word, "not found in lexicon!")
            return

        self.pointer += 1
        return packet

    def check_trig_req(self, packet: [Request]) -> (bool, Request):
        """
        check if there is a triggered Request in the packet. If yes, return the
        first triggered Request. If no, return an empty Request

        @param packet: word packet, a list of Requests
        @return: (boolean, Request)
        """
        for req in packet:
            if req.TEST_VAL:
                self.evaluate_test_val(req)

        # at this moment, the first request in the packet that has a True test
        # value will be triggered and returned. However, it is possible that multiple
        # requests in the packet have a True test value. We may need an algorithm to
        # help decide the request that has the highest priority.
        for req in packet:
            if req.TEST:
                print("\nREQUEST TRIGGERED: %s" % req.TEXT)
                return True, req

        return False, Request()

    def evaluate_test_val(self, req: Request):
        req.TEST = True
        for var in req.TEST_VAL:
            if req.TEST_VAL[var] != self.val[var]:
                req.TEST = False
                break

    def execute_assign(self, req: Request):
        """
        execute assignments in the Request

        @param req:
        @return:
        """
        print("\nASSIGNMENTS EXECUTED:")
        for var in req.ASSIGN_VAL:
            self.val[var] = req.ASSIGN_VAL[var]
            print(" - SET %s TO %s" % (var, req.ASSIGN_VAL[var]))
