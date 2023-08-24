# Blood enters the right side of your heart.
# Propara 310
from analyzer import Request, Packet, Analyzer

# todo: add check_parallel_noun to noun
lex = dict()
lex["*START*"] = Packet([Request(text="start parsing", test_flag=True,
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
                                                      assigns={"SUBJECT": "*CD"},
                                                      next=Packet([Request(text="PART-OF-SPEECH is verb",
                                                                           tests={"PART-OF-SPEECH": "verb"},
                                                                           assigns={"CONCEPT": "*CD"})]))]))])

################################################################################
lex["BLOOD"] = Packet([Request(text="noun BLOOD", test_flag=True,
                               assigns={"CD": "BLOOD", "PART-OF-SPEECH": "noun-phrase"})])

# revised enters
# lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True,
#                                 assigns={"CD": "ENTERS", "PART-OF-SPEECH": "verb"},
#                                 calls=[["PTRANS", "SUBJECT", None, None]],
#                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
#                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
#                                                      # todo: update or not...
#                                                      calls=[["UPDATEACT", "PTRANS", "to", "CD", None],
#                                                               ["PSTOP"], ["CONTAINED"], ["INGEST", None, None]])]))])
lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True,
                                assigns={"SUBJECT":"*CD","CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT","INGEST", "container", "CD", None], ["CONTAINED"]])]))])

lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])

lex["RIGHT"] = Packet([Request(text="adjective RIGHT", test_flag=True,
            assigns={"CD": "RIGHT", "PART-OF-SPEECH": "adjective"},
            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                 tests={"PART-OF-SPEECH": "noun-phrase"})]))])

lex["OF"] = Packet([Request(text="prep OF", test_flag=True,
                            assigns={"SUBJECT": "*CD", "CD": "OF", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase from lex OF",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["CONTAINED"], ["INGEST", "SUBJECT", "CD", None]])]))])

lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True,
                              assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["UPDATEACT", "INGEST", "from", "CD", None]])]))])

lex["YOUR"] = Packet([Request(text="possessive adjective YOUR", test_flag=True,
            assigns={"CD": "YOUR", "PART-OF-SPEECH": "possessive adjective"},
            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                 tests={"PART-OF-SPEECH": "noun-phrase"})]))])
lex["HEART"] = Packet([Request(text="noun HEART", test_flag=True,
                              assigns={"CD": "HEART", "PART-OF-SPEECH": "noun-phrase"})])

# Blood enters [add containment to side] the right side of [side - heart] your heart. [heart x contain blood] Blood travels to the lungs.
# trans in containment relationship: (A B) and (B C) = (A C)
lex["TRAVELS"] = Packet([Request(text="verb TRAVELS", test_flag=True,
                               assigns={"CD": "TRAVELS", "PART-OF-SPEECH": "verb"},
                               calls=[["PTRANS", "SUBJECT", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            # end the containment rl with the current subject. [mmp.py frame, ptrans function]. not in packet request.
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])

# lex["TRAVELS"] = Packet([Request(text="verb TRAVELS", test_flag=True,
#                                 assigns={"CD": "TRAVELS", "PART-OF-SPEECH": "verb"},
#                                 calls=[["PTRANS", "SUBJECT", None, None]],
#                                 next=Packet([Request(text="CD is FROM",
#                                                      tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
#                                              Request(text="CD is TO",
#                                                      tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])

# lex["TO"] = Packet([Request(text="prep TO", test_flag=True, assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
#                               next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
#                                                    tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
#                                                    calls=[["UPDATEACT", "PTRANS", "to", "CD", None],
#                                                           ["PSTOP"], ["CONTAINED"], ["INGESTED", None, None]])]))])

'''lex["TO"] = Packet([Request(text="prep TO", test_flag=True, assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None]]),
                                           Request(text="update an INGEST",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "INGEST": ""},
                                                   calls=[["UPDATEACT", "INGEST", "to", "CD", None]])]))])'''

lex["LUNGS"] = Packet([Request(text="noun LUNGS", test_flag=True,
                              assigns={"CD": "LUNGS", "PART-OF-SPEECH": "noun-phrase"})])

# Carbon dioxide is removed from the blood.
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})])
'''lex["IS"] = Packet([Request(text="helping verb IS", test_flag=True,
                            assigns={"CD": "IS", "PART-OF-SPEECH": "helping verb"},
                            next=Packet([Request(text="expecting a past participle of the main verb",
                                                 tests={"PART-OF-SPEECH": "verb"})]))])'''

lex["RELEASED"] = Packet([Request(text="verb RELEASED", test_flag=True,
                               assigns={"CD": "RELEASED","PART-OF-SPEECH": "verb"},
                               calls=[["EXPELED", None, None]])])

'''lex["INTO"] = Packet([Request(text="prep INTO", test_flag=True,
                              assigns={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","to","CD", None], ["CONTAINED"], ["INGESTED"]]),
                                          Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["CONTAINED"], ["INGESTED"]])]))])'''
'''lex["REMOVED"] = Packet([Request(text="verb REMOVED", test_flag=True,
                                 assigns={"CD": "REMOVED", "PART-OF-SPEECH": "verb"},
                                 calls=[["EXPELED", None, None]])])

lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True,
                              assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","from","CD", None], ["CONTAINED"], ["INGESTED", None,None]])]))])'''

lex["REMOVED"] = Packet([Request(text="verb REMOVED", test_flag=True,
                               assigns={"CD": "REMOVED","PART-OF-SPEECH": "verb"},
                               calls=[["EXPEL","SUBJECT", None, None]])])

lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True,
                              assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","container","CD", None], ["CONTAINED"], ["INGESTED", None, None]]),
                                          Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["CONTAINED"], ["INGESTED", None, None]])]))])

'''lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"})]))])'''

lex["RELEASE"] = Packet([Request(text="verb RELEASE", test_flag=True, assigns={"CD": "RELEASE", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["EXPEL", "CD", None]])]))])

lex["RELEASES"] = Packet([Request(text="verb RELEASES", test_flag=True,
                               assigns={"SUBJECT":"*CD", "CD": "RELEASES","PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["EXPEL", "CD", None]])]))])



# Oxygen is added to your blood.
lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                               assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])

'''lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    ),
                                            Request(text="contained",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    # assigns={"OBJECT": "*CD"},
                                                    # todo: ingested does not work
                                                    calls=[["CONTAINED"], ["INGEST","SUBJECT", None, None]])],
                                           keep=True))])'''
lex["RELEASED"] = Packet([Request(text="verb RELEASED", test_flag=True,
                               assigns={"CD": "RELEASED","PART-OF-SPEECH": "verb"},
                               calls=[["EXPEL", "SUBJECT", None, None]])])

lex["IS"] = Packet([Request(text="verb IS", test_flag=True,
                                assigns={"SUBJECT":"*CD", "CD": "IS", "PART-OF-SPEECH": "verb"})])

lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED","PART-OF-SPEECH": "verb"},
                               calls=[["INGEST", "SUBJECT", None, None]])])

lex["TO"] = Packet([Request(text="prep TO", test_flag=True,
                              assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None]]),
                                           Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","to","CD", None], ["INGEST", "CD", None, None],["CONTAINED"]]),
                                          Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase", "INGEST":""},
                                                    calls=[["UPDATEACT", "INGEST", "container", "CD", None], ["CONTAINED"]])]))])

'''
lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED","PART-OF-SPEECH": "verb"},
                               calls=[["INGEST", "SUBJECT", None, None]])])'''
'''
lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED", "PART-OF-SPEECH": "verb"},
                               calls=[["PTRANS", "SUBJECT", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])'''

'''lex["TO"] = Packet([Request(text="prep TO", test_flag=True,
                            assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None]]),
                                           Request(text="update an INGEST",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "INGEST": ""},
                                                   calls=[["UPDATEACT", "INGEST", "to", "CD", None]])]))])'''

'''lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED", "PART-OF-SPEECH": "verb"},
                               calls=[["INGEST", "SUBJECT", None, None],["CONTAINED"]],
                               next=Packet([Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
                                            Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])'''

lex["REACHES"] = Packet([Request(text="verb REACHES", test_flag=True,
                                assigns={"SUBJECT":"*CD", "CD": "REACHES", "PART-OF-SPEECH": "verb"},
                                calls=[["PTRANS", "SUBJECT", None, None],["CONTAINED"]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT","PTRANS", "to", "CD", None]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is TO",
                                                     tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])


# todo: generalization
lex["TRAPS"] = Packet([Request(text="verb TRAPS", test_flag=True, assigns={"CD": "TRAPS", "PART-OF-SPEECH": "verb"},
                               calls=[["CONTAIN"],["INGEST", None, None]], # todo: changed?
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    # w/o assigns
                                                    assigns={"OBJECT": "*CD"},
                                                    calls=[["CONTAIN"], ["INGEST", None, "SUBJECT"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                                                    )]))])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]])]))])

# Blood returns to left side of your heart.
# todo: returns? now it == enters, but is it always the case? returns = previously there but left, now return back. What to do: at previous frame, there is a containment of this relationship and expel.
# lex["TRAVELS"] = Packet([Request(text="verb TRAVELS", test_flag=True,
#                                assigns={"CD": "TRAVELS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
#                                next=Packet([Request(text="CD is TO",
#                                                     tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
#                                                     calls=[["ADVANCE TIME"]]),
#                                             # end the containment rl with the current subject. [mmp.py frame, ptrans function]. not in packet request.
#                                             Request(text="CD is FROM",
#                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
#                                            keep=True))])
# todo: side has "check contain"
lex["SIDE"] = Packet([Request(text="noun SIDE", test_flag=True,
                              assigns={"CD": "SIDE", "PART-OF-SPEECH": "noun-phrase"},
                              calls=[["CHECK CONTAIN"]])])
lex["BODY"] = Packet([Request(text="noun BODY", test_flag=True,
                              assigns={"CD": "BODY", "PART-OF-SPEECH": "noun-phrase"})])


lex["RETURNS"] = Packet([Request(text="verb RETURNS", test_flag=True,
                                 assigns={"CD": "RETURNS", "PART-OF-SPEECH": "verb"}, calls=[["INGEST","SUBJECT", None, None]]
                                 # calls=[["INGESTED", None, None],["CHECK CONTAIN"]],
                                )])
'''lex["TRAVELS"] = Packet([Request(text="verb TRAVELS", test_flag=True,
                               assigns={"CD": "TRAVELS", "PART-OF-SPEECH": "verb"},
                               calls=[["PTRANS", "SUBJECT", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])'''
'''lex["ADDED"] = Packet([Request(text="verb ADDED", test_flag=True,
                               assigns={"CD": "ADDED", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    ),
                                            Request(text="contained",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    # assigns={"OBJECT": "*CD"},
                                                    # todo: ingested does not work

                                                    calls=[["CONTAINED"], ["INGESTED", None, None]])],
                                           keep=True))])'''
# todo: get_containment does not work


# todo: get_containment(count),
lex["LEFT"] = Packet([Request(text="adjective LEFT", test_flag=True,
            assigns={"CD": "LEFT", "PART-OF-SPEECH": "adjective"},
            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase from lex LEFT",
                                 tests={"PART-OF-SPEECH": "noun-phrase"})]))])
# todo: heart contains side twice. none side contains blood?
# todo: lex['travels']=

lex["THROUGH"] = Packet([Request(text="prep THROUGH", test_flag=True, assigns={"CD": "THROUGH", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None],
                                                          ["PSTOP"], ["CONTAINED"], ["INGESTED", None, None]])]))])
analyzer = Analyzer(lexicon=lex)

# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
# print(analyzer.parse("plants absorb water"))
analyzer.parse("Blood enters the right side of your heart. Blood travels to the lungs. Carbon-dioxide is removed from the blood. Oxygen is added to your blood. Blood returns to left side of your heart. The blood travels through the body. ")
# analyzer.parse("The blood travels through the body.")
# todo: okay
# analyzer.parse("The rain falls on the soil from the cloud.")
# analyzer.parse("Jack and Susan have a ball.")

# print("\n\n\n.....................................................................")
# analyzer.model.print(0)
# analyzer.model.print(1)
# analyzer.model.advance_time()
# analyzer.model.print(2)
# print out all time steps.

# multiple calls, keep stack

# These pulmonary veins bring the oxygenated blood to the left atrium of the heart.
#
# The blood travels through the body: From the left atrium, the oxygenated blood is pumped into the left ventricle,
# and when the left ventricle contracts, it sends the oxygenated blood out through the main artery of the body, called
# the aorta. The aorta branches into smaller arteries, which carry the oxygenated blood to various organs and tissues
# throughout the body.
