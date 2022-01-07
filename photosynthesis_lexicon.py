# Roots absorb water from soil.
# The water flows to the leaf.
# Light from the sun and CO2 enter the leaf.
# The light, water, and CO2 combine into a mixture.
# Mixture forms sugar.


from analyzer import Request, Packet, Analyzer

lex = dict()
lex["*START*"] = Packet([Request(text="start parsing", test_flag=True,
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
                                                      assigns={"SUBJECT": "*CD"},
                                                      next=Packet([Request(text="PART-OF-SPEECH is verb",
                                                                           tests={"PART-OF-SPEECH": "verb"},
                                                                           assigns={"CONCEPT": "*CD"})]))]))])

# nouns: roots, water, soil, leaf, light, sun, CO2, mixture, sugar
lex["ROOTS"] = Packet([Request(text="noun ROOTS", test_flag=True,
                               assigns={"CD": "ROOTS", "PART-OF-SPEECH": "noun-phrase"})])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])
lex["LEAF"] = Packet([Request(text="noun LEAF", test_flag=True,
                              assigns={"CD": "LEAF", "PART-OF-SPEECH": "noun-phrase"})])
lex["LIGHT"] = Packet([Request(text="noun LIGHT", test_flag=True,
                               assigns={"CD": "LIGHT", "PART-OF-SPEECH": "noun-phrase"})])
lex["SUN"] = Packet([Request(text="noun SUN", test_flag=True,
                             assigns={"CD": "SUN", "PART-OF-SPEECH": "noun-phrase"})])
lex["CO2"] = Packet([Request(text="noun CO2", test_flag=True,
                             assigns={"CD": "CO2", "PART-OF-SPEECH": "noun-phrase"})])
lex["MIXTURE"] = Packet([Request(text="noun MIXTURE", test_flag=True,
                                 assigns={"CD": "MIXTURE", "PART-OF-SPEECH": "noun-phrase"})])
lex["SUGAR"] = Packet([Request(text="noun SUGAR", test_flag=True,
                               assigns={"CD": "SUGAR", "PART-OF-SPEECH": "noun-phrase"})])

# verbs: absorb, flows, enter, combine, forms
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["FLOWS"] = Packet([Request(text="verb FLOWS", test_flag=True,
                               assigns={"CD": "FLOWS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"], ["PSTOP"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])  # @todo advance time at the verb "flows"
lex["ENTER"] = Packet([Request(text="verb ENTER", test_flag=True, assigns={"CD": "ENTER", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAINED"]])]))])
# lex["COMBINE"] =
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True, assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])

# prepositions and others: the, from, to
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])
# @todo absorb from?
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD",
                                                           None]])]))])
lex["TO"] = Packet([Request(text="prep TO", test_flag=True, assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["UPDATEACT", "PTRANS", "to", "CD", None]])]))])

analyzer = Analyzer(lexicon=lex)
# analyzer.parse("The water flows to the leaf.")
# analyzer.parse("Light from the sun and CO2 enter the leaf.")
# analyzer.parse("CO2 enter the leaf.")
# analyzer.parse("Mixture forms sugar.")
