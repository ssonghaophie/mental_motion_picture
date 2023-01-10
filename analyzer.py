from mental_model import MentalMotionPicture
import re  # regular expression


# Each word entry in the lexicon is a word packet,
# which is a list of Request objects with some flags
class Request:

    def __init__(self, text=None, test_flag=False, tests=None, assigns=None, calls=None, next=None):
        self.TEXT = text  # short explanation of the Request
        self.TEST_FLAG = test_flag  # boolean
        self.TESTS = tests  # if all evaluations pass, set test to be True
        self.ASSIGNS = assigns  # assignments to complete if test==True
        self.CALLS = calls  # mental model function calls
        self.NEXT_PACKET = next


class Packet:

    def __init__(self, requests: [Request], keep=False, one_time=False):
        self.requests = requests
        self.keep = keep
        self.one_time = one_time  # doc for one_time


# the ELI analyzer
class Analyzer:
    model = MentalMotionPicture()
    cur_word = None

    # to keep track of the parsing progress of the analyzer
    # vars = {"CD": None, "PART-OF-SPEECH": None, "SUBJECT": None, "OBJECT": None}
    # todo: both subject and object can be multiple things, maybe a list??
    vars = {"CD": None, "PART-OF-SPEECH": None, "SUBJECT": [], "OBJECT": []}

    # todo: maybe each property should be its own attribute of the analyzer??
    # cd = None
    # part_of_speech = None
    # subject = []
    # object = []

    # to keep track of parallel noun phrases and noun combinations
    noun = False
    first_noun = True  # encounter the first noun of a group of parallel noun phrases
    noun_parallel = []  # some nouns phrases are parallel but the paragraph doesn't define them as a combo
    noun_combo = []  # the paragraph defines them to be combinations / mixture

    def __init__(self, lexicon: {}):
        self.paragraph = []  # a paragraph is a list of sentences
        self.sentence = []  # a sentence is a list of words
        self.stack = []  # store word packets
        self.triggered = []  # triggered requests
        self.cd = None  # the output, what data structure?
        self.lexicon = lexicon

        # read words from sentence
        self.length = 0  # length of the SENTENCE list
        self.pointer = 0  # index of the next word in SENTENCE

    def parse(self, text: str):
        """
        construct and run an analyzer

        @param text: input text
        # @return:
        """
        self.split_paragraph(text)
        print(self.paragraph)
        while self.paragraph:
            self.length = 0  # length of the SENTENCE list
            self.pointer = 0  # index of the next word in SENTENCE

            # if the most recent Frame is empty, then we must be parsing the
            # first sentence of the paragraph; otherwise, advance Frame when
            # parsing a new sentence
            if not self.model.cur.empty:
                self.model.advance_time()

            sentence = self.paragraph.pop(0)
            self.split_sentence(sentence)
            print("\n", self.sentence)
            print("--------------------------------------------------------")
            print("SENTENCE:", end=" ")
            for word in self.sentence[1:]:
                print(word, end=" ")
            print()

            # todo: make it a function?? reset the analyzer attributes
            for var in self.vars:
                self.vars[var] = None

            # loop 1 - terminates when SENTENCE is empty
            while self.pointer < self.length:
                # read next word, put packet on top of stack
                self.stack.append(self.read_word())
                self.noun = False
                self.first_noun = True

                # loop 2
                while self.stack:
                    trig_flag, trig_req = self.check_trig_req(self.stack[-1])
                    if trig_flag:
                        self.triggered.append(trig_req)

                        # keep flag is True, keep the packet but remove the request.
                        if self.stack[-1].keep:
                            self.stack[-1].requests.remove(trig_req)
                            # if after removal, the packet is empty, remove the packet
                            if not self.stack[-1].requests:
                                self.stack.pop()
                        # keep flag is False, remove the packet
                        else:
                            self.stack.pop()

                        if trig_req.ASSIGNS:
                            self.execute_assign(trig_req)
                        if trig_req.CALLS:
                            self.function_call(trig_req)
                        continue

                    elif not self.stack[-1]:  # word not in lexicon
                        self.stack.pop()
                        continue

                    # (for the parallel noun phrase functionality) if the packet should be checked only one time,
                    # then even if no request is triggered, remove the packet from stack
                    elif self.stack[-1].one_time:
                        self.stack.pop()
                    break

                # loop 3
                while self.triggered:
                    cur_request = self.triggered.pop()
                    if cur_request.NEXT_PACKET:
                        self.stack.append(cur_request.NEXT_PACKET)

                    if cur_request.TEXT == "check parallel noun-phrases":
                        self.first_noun = False

                # group noun phrases into parallel groups
                if self.noun:
                    if self.first_noun:
                        self.noun_parallel.append([self.cur_word])
                    else:  # it is a noun but not the first one of a group of parallel noun phrases
                        self.noun_parallel[-1].append(self.cur_word)

        self.print_results()

    def print_results(self):
        print("\n--------------------------------------------------------")
        print("|||||||||||||||||||||| THE END |||||||||||||||||||||||||")
        print("--------------------------------------------------------\n")

        # print packets left on stack
        print(len(self.stack), "word packet(s) left on STACK:")
        for packet in self.stack:
            print(" -", packet.requests[0].TEXT)

        # print the resulting mental model
        print("\n--------------------------------------------------------")
        print("mental model generated:")
        print("\nparallel noun phrases", self.noun_parallel)
        print("noun phrase combinations", self.noun_combo)
        self.model.print_latest()

        # print("vars of the analyzer:", self.vars)

    def split_paragraph(self, para: str):
        self.paragraph = re.split(r"[,.!?]\s", para)

    def split_sentence(self, sentence: str):
        """
        the input sentence is put into uppercase and split on all
        whitespace strings. The resulted list is appended on SENTENCE

        @param sentence: input sentence
        """
        # remove leading and trailing characters and put into uppercase
        sentence = "*START* " + sentence.strip(".,?;:/\\ !@#$%^&*").upper()

        # split on whitespace characters
        self.sentence = sentence.split()
        self.length += len(self.sentence)

    def read_word(self) -> Packet:
        """
        read the next word from self.SENTENCE, find the word in
        lexicon, and return the word packet

        @return: a word packet in the lexicon
        """
        self.cur_word = self.sentence[self.pointer]
        print("--------------------------------------------------------")
        print("READ WORD: %s" % self.cur_word)

        # check if the word has an entry in the lexicon
        if self.cur_word in self.lexicon:
            packet = self.lexicon[self.cur_word]
        else:
            print(self.cur_word, "not found in lexicon!")
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

                # if the word is a noun, add to maps
                if req.TEXT.startswith("noun"):
                    self.model.add_object(req.TEXT[5:])

                return True, req

        return False, Request()

    def evaluate_tests(self, req: Request):
        req.TEST_FLAG = True
        for var in req.TESTS:
            # if the request is UPDATEACT, check if a primitive act exist
            if var in ("PTRANS", "PSTOP", "INGEST", "EXPEL"):
                if not self.model.cur.actions_by_type[var]:
                    req.TEST_FLAG = False
                    break
            elif req.TESTS[var] != self.vars[var]:
                req.TEST_FLAG = False
                break

    def execute_assign(self, req: Request):
        """
        execute assignments in the Request

        @param req:
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

            # check if "PART-OF-SPEECH" is "noun-phrase" and update self.noun
            if var == "PART-OF-SPEECH" and req.ASSIGNS[var] == "noun-phrase":
                self.noun = True

    def function_call(self, req: Request):
        calls = req.CALLS
        print("\nFUNCTION CALL(S) TO MENTAL MOTION PICTURE:")
        for call in calls:
            if call[0] == "CONTAIN":  # active
                print(" - %s CONTAIN(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.contain((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "CONTAINED":  # passive!
                print(" - %s CONTAIN(S) %s" % (self.vars["CD"], self.vars["SUBJECT"]))
                self.model.contain((self.vars["CD"], self.vars["SUBJECT"]))

            elif call[0] == "INGEST":  # active
                print(" - %s INGEST(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.INGEST(object=self.vars["CD"], container=self.vars["SUBJECT"])

            elif call[0] == "INGESTED":  # passive!
                print(" - %s INGEST(S) %s" % (self.vars["CD"], self.vars["SUBJECT"]))
                self.model.INGEST(object=self.vars["SUBJECT"], container=self.vars["CD"])

            elif call[0] == "STATECHANGE":
                print(" - %s BECOME(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.STATECHANGE(object=self.vars["SUBJECT"], to=self.vars["CD"])

            elif call[0] == "ABOVE":
                print(" - %s IS/ARE ABOVE %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.above((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "UNDER":
                print(" - %s IS/ARE UNDER %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.under((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "PTRANS":
                ptrans_to = call[1]
                ptrans_from = call[2]
                print(" - %s MOVE(s) FROM %s TO %s" % (self.vars["SUBJECT"], ptrans_from, ptrans_to))
                self.model.PTRANS(object=self.vars["SUBJECT"], to=ptrans_to, From=ptrans_from)

            elif call[0] == "PSTOP":
                print(" - %s STOP(S) MOVING..." % self.vars["SUBJECT"])
                self.model.PSTOP(self.vars["SUBJECT"])

            elif call[0] == "ADVANCE TIME":
                # print(" - ADVANCE TO TIME-STEP", self.model.count + 1)
                self.model.advance_time()

            elif call[0] == "UPDATEACT":
                print(" - UPDATE ACT", call[1])
                if call[3] == "CD":
                    call[3] = self.vars["CD"]
                self.model.update_act_by_type(call[1], call[2], call[3], call[4])

            elif call[0] == "UPDATEACT ADD OBJECT":
                print(" - UPDATE ACT & ADD OBJECT")
                if call[1] == "CD":
                    call[1] = self.vars["CD"]
                self.model.update_act_add_object(call[1])

            # parallel noun phrases and combinations!
            elif call[0] == "DEFINE COMBO":
                if self.noun_parallel:
                    self.noun_combo.append(self.noun_parallel[-1])
                    print(" - %s is a noun phrase combination" % self.noun_parallel[-1])

            elif call[0] == "MATCH COMBO":
                if self.noun_combo:
                    print(" - %s equals combination %s" % (self.cur_word, self.noun_combo[-1]))
                elif self.noun_parallel:
                    # todo: iterate backwards to find the first combo (len > 1)
                    pass
                    # print(" - %s equals combination %s" % (self.cur_word, self.noun_parallel[-1]))

            # special words have their own function calls
            # todo - how does the analyzer handle the special word "as"?
            # create a timestep before the latest one,
            # and make any changes to the newly inserted timestep
            elif call[0] == "SPECIAL":
                pass

            else:
                print("Invalid function call to mental motion picture!")
