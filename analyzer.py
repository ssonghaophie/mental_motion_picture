from map import Containment, Space, Touching
from mental_model import Time_step, Mental_model


# Each word entry in the lexicon is a list of Request objects with a keep flag
class Request:

    def __init__(self, text=None, test_flag=False, tests=None, assigns=None, calls=None, next=None):
        self.TEXT = text  # short explanation of the Request
        self.TEST_FLAG = test_flag  # boolean
        self.TESTS = tests  # if all evaluations pass, set test to be True
        self.ASSIGNS = assigns  # assignments to complete if test==True
        self.CALLS = calls  # mental model function calls
        self.NEXT_PACKET = next


class Packet:

    def __init__(self, requests: [Request], keep=False):
        self.requests = requests
        self.keep = keep


# the ELI analyzer
class Analyzer:
    vars = {"CD": None, "PART-OF-SPEECH": None, "SUBJECT": None, "OBJECT": None}
    model = Mental_model(Containment(), Space(), Touching())

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
        # @return:
        """
        self.split(sentence)
        print("--------------------------------------------------------")
        print("SENTENCE:", end=" ")
        for word in self.SENTENCE[1:]:
            print(word, end=" ")
        print()

        # loop 1 - terminates when SENTENCE is empty
        while self.pointer < self.length:
            # read next word, put packet on top of stack
            self.STACK.append(self.read_word())

            # loop 2
            while self.STACK:
                trig_flag, trig_req = self.check_trig_req(self.STACK[-1])
                if trig_flag:
                    self.TRIGGERED.append(trig_req)

                    # keep flag is True, keep the packet but remove the request.
                    if self.STACK[-1].keep:
                        self.STACK[-1].requests.remove(trig_req)
                        # if after removal, the packet is empty, remove the packet
                        if not self.STACK[-1].requests:
                            self.STACK.pop()
                    # keep flag is False, remove the packet
                    else:
                        self.STACK.pop()

                    if trig_req.ASSIGNS:
                        self.execute_assign(trig_req)
                    if trig_req.CALLS:
                        self.function_call(trig_req)
                    continue

                elif not self.STACK[-1]:  # word not in lexicon
                    self.STACK.pop()
                    continue
                break

            # loop 3
            while self.TRIGGERED:
                cur_request = self.TRIGGERED.pop()
                if cur_request.NEXT_PACKET:
                    self.STACK.append(cur_request.NEXT_PACKET)

        # if anything left on the stack, print it
        print("\n--------------------------------------------------------")
        print("|||||||||||||||||||||| THE END |||||||||||||||||||||||||")
        print("--------------------------------------------------------\n")

        # print packets left on stack
        print(len(self.STACK), "word packet(s) left on STACK:")
        for packet in self.STACK:
            print(" -", packet.requests[0].TEXT)

        # print the resulting mental model
        print("\n--------------------------------------------------------")
        print("mental model generated:")
        self.model.print_latest()

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

    def read_word(self) -> Packet:
        """
        read the next word from self.SENTENCE, find the word in
        lexicon, and return the word packet

        @return:
        """
        word = self.SENTENCE[self.pointer]
        print("--------------------------------------------------------")
        print("READ WORD: %s" % word)

        # check if the word has an entry in the lexicon
        if word in self.LEXICON:
            packet = self.LEXICON[word]
        else:
            print(word, "not found in lexicon!")
            packet = None

        self.pointer += 1
        return packet

    def check_trig_req(self, packet: Packet) -> (bool, Request):
        """
        check if there is a triggered Request in the packet. If yes, return the
        first triggered Request. If no, return an empty Request

        @param packet: word packet, a list of Requests
        @return: (boolean, Request)
        """
        if not packet:
            return False, None

        for req in packet.requests:
            if req.TESTS:
                self.evaluate_tests(req)

        # at this moment, the first request in the packet that has a True test
        # value will be triggered and returned. However, it is possible that multiple
        # requests in the packet have a True test value. We may need an algorithm to
        # help decide the request that has the highest priority.
        for req in packet.requests:
            if req.TEST_FLAG:
                print("\nREQUEST TRIGGERED: %s" % req.TEXT)
                return True, req

        return False, Request()

    def evaluate_tests(self, req: Request):
        req.TEST_FLAG = True
        for var in req.TESTS:
            if req.TESTS[var] != self.vars[var]:
                req.TEST_FLAG = False
                break

    def execute_assign(self, req: Request):
        """
        execute assignments in the Request

        @param req:
        @return:
        """
        print("\nASSIGNMENT(S) EXECUTED:")
        for var in req.ASSIGNS:
            # print(req.ASSIGNS[var])
            if req.ASSIGNS[var][0] == "*":
                s = self.vars[req.ASSIGNS[var][1:]]
                self.vars[var] = s
                print(" - SET %s TO %s(=%s)" % (var, req.ASSIGNS[var][1:], s))
            else:
                self.vars[var] = req.ASSIGNS[var]
                print(" - SET %s TO %s" % (var, req.ASSIGNS[var]))

    def function_call(self, req: Request):
        calls = req.CALLS
        print("\nFUNCTION CALL(S) TO MENTAL MODEL:")
        for call in calls:
            if call[0] == "CONTAIN":
                print(" - %s CONTAIN(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.contain((self.vars["SUBJECT"], self.vars["CD"]))
                self.model.INGEST(object=self.vars["CD"], container=self.vars["SUBJECT"])

            elif call[0] == "STATECHANGE":
                print(" - %s BECOME(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.STATECHANGE(object=self.vars["SUBJECT"], to=self.vars["CD"])

            elif call[0] == "ABOVE":
                print(" - %s IS/ARE ABOVE %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.above((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "PTRANS":
                to = call[1]
                From = call[2]
                print(" - %s MOVE(s) FROM %s TO %s" % (self.vars["SUBJECT"], From, to))
                self.model.PTRANS(object=self.vars["SUBJECT"], to=to, From=From)

            elif call[0] == "PSTOP":
                print(" - %s STOP(S) MOVING..." % self.vars["SUBJECT"])
                self.model.PSTOP(self.vars["SUBJECT"])

            elif call[0] == "ADVANCE TIME":
                print(" - ADVANCE TO TIME-STEP")
                self.model.advance_time()
