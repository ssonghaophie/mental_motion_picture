from mental_motion_picture import MentalMotionPicture
from packet import Packet
from request import Request
import re  # regular expression


# the ELI analyzer
class Analyzer:
    model = MentalMotionPicture()
    cur_word = None
    cur_sentence = None

    # to keep track of the parsing progress of the analyzer
    # vars = {"CD": None, "PART-OF-SPEECH": None, "SUBJECT": None, "OBJECT": None}
    # todo: both subject and object can be multiple things, maybe a list??
    vars = {"CD": "None", "PART-OF-SPEECH": "None", "SUBJECT": "None", "OBJECT": []}

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

            self.cur_sentence = self.paragraph.pop(0)
            self.model.cur_sentence = self.cur_sentence
            self.model.cur.sentence = self.cur_sentence

            self.split_sentence(self.cur_sentence)
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
                        
            # CHANGE: print the mental model generated for every frame
            print("\n--------------------------------------------------------")
            print("mental model generated:")
            self.model.print_latest()

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
        # print("\nparallel noun phrases", self.noun_parallel)
        # print("noun phrase combinations", self.noun_combo)
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
        read the next word of the sentence, find the word in
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
                    self.model.add_to_graph(req.TEXT[5:])

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
    
    def check_containment(self):
            print("Checking for exist containment")
            return self.model.check_containment_exist()

    def function_call(self, req: Request):
        act_obj = None
        act_container = None
        act_to = None
        act_from = None
        obj_changed = None
        calls = req.CALLS
        print("\nFUNCTION CALL(S) TO MENTAL MOTION PICTURE:")
        for call in calls:

            if call[0] == "CONTAIN":  # active
                print(" - %s CONTAIN(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.contain((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "CONTAINED":  # passive!
                print(" - %s CONTAIN(S) %s" % (self.vars["CD"], self.vars["SUBJECT"]))
                self.model.contain((self.vars["CD"], self.vars["SUBJECT"]))

            elif call[0] == "CHECK CONTAIN":  # todo: new added!
                print("Checking for exist containment")
                result = self.model.check_containment_exist()
                print(result)

            # CHANGE: make INGEST and INGESTED be able to be updated
            elif call[0] == "INGEST":  # active
                global ingest_obj
                global ingest_container
                if call[1]:
                    act_obj=self.vars[call[1]]
                if call[2]:
                    act_container = self.vars[call[2]]
                if call[3]:
                    act_from = self.vars[call[3]]
                ingest_to = self.vars["SUBJECT"]
                ingest_obj=self.vars["CD"]
                ingest_container=ingest_to
                print(" - %s INGEST(S) %s FROM %s" % (act_container, act_obj, act_from))
                self.model.ingest(obj=act_obj, container=act_container, ingest_from=act_from)
                #print(" - %s INGEST(S) %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                #self.model.ingest(obj=ingest_obj, container=ingest_container)

            # elif call[0] == "INGESTED":  # passive!
            #     if call[1]:
            #         act_obj=self.vars[call[1]]
            #     if call[2]:
            #         act_container = self.vars[call[2]]
            #     if call[3]:
            #         act_from = self.vars[call[3]]
            #     print(" - %s INGEST(S) %s FROM %s" % (act_container, act_obj, act_from))
            #     self.model.ingest(obj=act_obj, container=act_container, ingest_from=act_from)

            # CHANGE: make EXPEL and EXPELED be able to be updated, and add container if there exist containment relationship
            elif call[0] == "EXPEL":  # active
                if call[1]:
                    act_obj=self.vars[call[1]]
                if call[2]:
                    act_from = self.vars[call[2]]
                if call[3]:
                    act_to = self.vars[call[3]]
                # if 'ingest_obj' in globals():
                #     if self.vars["SUBJECT"] == ingest_obj:
                #         expel_from=ingest_container
                print(" - %s EXPEL(S) %s TO %s" % (act_from, act_obj, act_to))
                self.model.expel(obj=act_obj, container=act_from, expel_to=act_to)

            # elif call[0] == "EXPELED":  # passive
            #     expel_from=call[1]
            #     expel_to=call[2]
            #     if 'ingest_obj' in globals():
            #         if self.vars["SUBJECT"] == ingest_obj:
            #             expel_from=ingest_container
            #     print(" - %s EXPEL(S) %s TO %s" % (expel_from, self.vars["SUBJECT"], expel_to))
            #     self.model.expel(obj=self.vars["SUBJECT"], container=expel_from, expel_to=expel_to)

            elif call[0] == "STATECHANGE":
                if call[1]:
                    act_obj=self.vars[call[1]]
                if call[2]:
                    if call[2] == "SUBJECT" or call[2] == "CD":
                        obj_changed = self.vars[call[2]]
                    else:
                        obj_changed = call[2]
                print(" - %s BECOME(S) %s" % (act_obj, obj_changed))
                if act:
                    obj1 = self.model.cur.space.noun_dict[self.vars["SUBJECT"]]
                    obj2 = self.model.cur.space.noun_dict[self.vars["CD"]]
                    obj2.combo = obj1.combo
                self.model.state_change(obj=self.vars["SUBJECT"], to=self.vars["CD"])

            elif call[0] == "ABOVE":
                print(" - %s IS/ARE ABOVE %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.above((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "UNDER":
                print(" - %s IS/ARE UNDER %s" % (self.vars["SUBJECT"], self.vars["CD"]))
                self.model.under((self.vars["SUBJECT"], self.vars["CD"]))

            elif call[0] == "PTRANS":
                if call[1]:
                    act_obj=self.vars[call[1]]
                if call[2]:
                    act_to = self.vars[call[2]]
                if call[3]:
                    act_from = self.vars[call[3]]
                print(" - %s MOVE(s) FROM %s TO %s" % (act_obj, act_from, act_to))
                self.model.ptrans(obj=act_obj, to=act_to, act_from=act_from)

            elif call[0] == "PSTOP":
                print(" - %s STOP(S) MOVING..." % self.vars["SUBJECT"])
                self.model.pstop(self.vars["SUBJECT"])

            elif call[0] == "ADVANCE TIME":
                self.model.advance_time()

            elif call[0] == "UPDATEACT":
                print(" - UPDATE ACT", call[1])
                if call[3] == "CD":
                    call[3] = self.vars["CD"]
                if call[4] == "CD":
                    call[4] = self.vars["CD"]
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
                combo_str = None
                combo = []
                if self.noun_combo:
                    combo_str = self.noun_combo[-1]
                elif self.noun_parallel:
                    i = -1
                    while (not combo_str) and (len(self.noun_parallel) + i >= 0):
                        if len(self.noun_parallel[i]) > 1:
                            combo_str = self.noun_parallel[i]
                        else:
                            i -= 1
                for noun_str in combo_str:
                    noun_obj = self.model.cur.space.noun_dict[noun_str]
                    combo.append(noun_obj)
                self.model.cur.space.noun_dict[self.cur_word].combo = combo
                print(" - %s equals combination %s" % (self.cur_word, combo_str))

            # special words have their own function calls
            # todo - how does the analyzer handle the special word "as"?
            # create a timestep before the latest one,
            # and make any changes to the newly inserted timestep
            elif call[0] == "SPECIAL":
                pass

            else:
                print("Invalid function call to mental motion picture!")
