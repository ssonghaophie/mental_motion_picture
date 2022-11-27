# Paragraph 31 - how do caverns form?
# 1. Limestone is located under the soil.
# 2. Rain picks up carbon dioxide as it falls to earth.
# 3. The rain falls on the soil over the limestone.
# -- 4. The carbon dioxide in the rain washes through the soil.
# 5. The carbon dioxide turns into acid.
# 6. The acid in the rain gets to the limestone below the soil.
# -- 7. The acid dissolves the limestone.
# -- 8. Acid continues to erode the limestone with more rain over time.
# 9. The eroded limestone sometimes forms caves.

################################################################################
from analyzer import Request, Packet, Analyzer

lex = dict()
lex["*START*"] = Packet([Request(text="start parsing", test_flag=True,
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
                                                      assigns={"SUBJECT": "*CD"},
                                                      next=Packet([Request(text="PART-OF-SPEECH is verb",
                                                                           tests={"PART-OF-SPEECH": "verb"},
                                                                           assigns={"CONCEPT": "*CD"})]))]))])
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])

# 1. Limestone is located under the soil.
lex["LIMESTONE"] = Packet([Request(text="noun LIMESTONE", test_flag=True,
                                   assigns={"CD": "LIMESTONE", "PART-OF-SPEECH": "noun-phrase"})])
lex["IS"] = Packet([Request(text="verb IS", test_flag=True,
                            assigns={"CD":"IS", "PART-OF-SPEECH": "verb"})])
lex["LOCATED"] = Packet([Request(text="verb LOCATED", test_flag=True,
                                 assigns={"CD": "UNDER", "PART-OF-SPEECH": "preposition"})])
lex["UNDER"] = Packet([Request(text="prep UNDER", test_flag=True,
                               assigns={"CD": "UNDER", "PART-OF-SPEECH": "preposition"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["UNDER"]])]))])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])

# 2. Rain picks up carbon dioxide as it falls to earth. (Rain picks up carbon-dioxides.)
lex["RAIN"] = Packet([Request(text="noun RAIN", test_flag=True,
                              assigns={"CD": "RAIN", "PART-OF-SPEECH": "noun-phrase"})])
lex["PICKS"] = Packet([Request(text="verb PICKS", test_flag=True,
                               assigns={"CD": "PICKS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["CONTAIN"]])]))])
lex["UP"] = Packet([Request(text="prep UP", test_flag=True,
                            assigns={"CD": "UP", "PART-OF-SPEECH": "preposition"})])
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})])

# todo - "AS" - insert a timestep before the most current one?
# a special word that should be predefined in the analyzer

lex["AS"] = Packet([Request(text="", test_flag=True, assigns={"CD": "AS"}, calls=[["SPECIAL", "AS"]])])
lex["IT"] = Packet([Request(text="noun IT", test_flag=True,
                            assigns={"CD": "*SUBJECT", "PART-OF-SPEECH": "noun-phrase"})])
lex["FALLS"] = Packet([Request(text="verb FALLS", test_flag=True,
                               assigns={"CD": "FALLS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", "EARTH", None]],
                               next=Packet([Request(text="CD is ON",
                                                    tests={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"], ["PSTOP"]]),
                                            Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"}),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])
lex["TO"] = Packet([Request(text="prep TO", test_flag=True,
                            assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["UPDATEACT", "PTRANS", "to", "CD", None]])]))])
lex["EARTH"] = Packet([Request(text="noun EARTH", test_flag=True,
                               assigns={"CD": "EARTH", "PART-OF-SPEECH": "noun-phrase"})])

# 3. The rain falls on the soil over the limestone. (The rain falls on the soil.)
lex["ON"] = Packet([Request(text="prep ON", test_flag=True,
                            assigns={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["UPDATEACT", "PTRANS", "to", "CD", None], ["ABOVE"]])]))])

# todo - 4. The carbon dioxide in the rain washes through the soil.
# replace washes with moves
# gets into
# goes into

# 5. The carbon-dioxide turns into acid.
lex["TURNS"] = Packet([Request(text="verb TURNS", test_flag=True,
                               assigns={"CD": "TURNS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is preposition",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"}),
                                            Request(text="PART-OF-SPEECH is preposition",
                                                    tests={"CD": "INTO", "PART-OF-SPEECH": "preposition"})]))])
lex["INTO"] = Packet([Request(text="prep INTO", test_flag=True,
                              assigns={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["ACID"] = Packet([Request(text="noun ACID", test_flag=True, assigns={"CD": "ACID", "PART-OF-SPEECH": "noun-phrase"})])

# 6. The acid in the rain gets to the limestone below the soil.
# in the rain/below the soil
lex["IN"] = Packet([Request(text="prep IN", test_flag=True,
                            assigns={"CD": "IN", "PART-OF-SPEECH": "preposition"})])
lex["GETS"] = Packet([Request(text="verb GETS", test_flag=True,
                              assigns={"CD": "GETS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                              next=Packet([Request(text="CD is TO",
                                                   tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])
lex["BELOW"] = Packet([Request(text="prep BELOW", test_flag=True,
                               assigns={"CD": "BELOW", "PART-OF-SPEECH": "preposition"})])

# todo - 7. The acid dissolves the limestone.
# lex["DISSOLVES"]

# todo - 8. Acid continues to erode the limestone with more rain over time.
# the limestone disappears into the acid
# statechange? limestone becomes acid? (solid -> liquid)
# limestone and acid become one?
# maybe get rid off continues/over time/more for now?

# 9. The eroded limestone sometimes forms caves.
# todo - adjectives, frequency
lex["ERODED"] = Packet([Request(text="adjective ERODED", test_flag=True,
                                assigns={"CD": "ERODED", "PART-OF-SPEECH": "adjective"})])
lex["SOMETIMES"] = Packet([Request(text="adverb SOMETIMES", test_flag=True,
                                   assigns={"CD": "SOMETIMES", "PART-OF-SPEECH": "adverb"})])
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True,
                               assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["CAVES"] = Packet([Request(text="noun CAVES", test_flag=True,
                               assigns={"CD": "CAVES", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)
sentence = "Limestone is located under the soil. Rain picks up carbon-dioxide as it falls to earth. The rain falls on the soil. The carbon-dioxide turns into acid. The acid in the rain gets to the limestone below the soil. The eroded limestone sometimes forms caves."
analyzer.parse(sentence)

# analyzer.parse("Limestone is located under the soil.")
# analyzer.parse("Rain picks up carbon-dioxide as it falls to earth.")
# analyzer.parse("The rain falls on the soil over the limestone.")
# analyzer.model.print(1)
# analyzer.model.print(2)
