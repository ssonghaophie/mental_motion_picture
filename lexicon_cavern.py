# Paragraph 31 - how do caverns form?
# 1. Limestone is located under the soil.
# 2. Rain picks up carbon dioxide as it falls to earth.
# 3. The rain falls on the soil over the limestone.
# 4. The carbon dioxide in the rain washes through the soil.
# 5. The carbon dioxide turns into acid.
# 6. The acid in the rain gets to the limestone below the soil.
# 7. The acid dissolves the limestone.
# 8. Acid continues to erode the limestone with more rain over time.
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

# simplify sentence 2 and 3 to
# Rain picks up carbon-dioxides. The rain falls on the soil.
lex["RAIN"] = Packet([Request(text="noun RAIN", test_flag=True,
                              assigns={"CD": "RAIN", "PART-OF-SPEECH": "noun-phrase"})])
lex["PICKS"] = Packet([Request(text="verb PICKS", test_flag=True,
                               assigns={"CD": "PICKS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["CONTAIN"]])],
                                           keep=True))])
lex["UP"] = Packet([Request(text="prep UP", test_flag=True,
                            assigns={"CD": "UP", "PART-OF-SPEECH": "preposition"})])
lex["CARBON-DIOXIDES"] = Packet([Request(text="noun CARBON-DIOXIDES", test_flag=True,
                              assigns={"CD": "CARBON-DIOXIDES", "PART-OF-SPEECH": "noun-phrase"})])
lex["FALLS"] = Packet([Request(text="verb FALLS", test_flag=True,
                               assigns={"CD": "FALLS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", "EARTH", None]],
                               next=Packet([Request(text="CD is ON",
                                                    tests={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"], ["PSTOP"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])
lex["ON"] = Packet([Request(text="prep ON", test_flag=True,
                            assigns={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["UPDATEACT", "PTRANS", "to", "CD", None], ["ABOVE"]])]))])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)
analyzer.parse("Rain picks up carbon-dioxides. The rain falls on the soil.")
# analyzer.parse("Rain picks up carbon-dioxides.")

analyzer.model.print(1)
analyzer.model.print(2)
