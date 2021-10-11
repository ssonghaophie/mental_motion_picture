from analyzer import Request, Packet, Analyzer

# lexicon should be a hash table (python dictionary)
# key - the word
# value - definition of the word (a list of request objects)
lex = dict()
lex["*START*"] = Packet([Request(text="start parsing", test_flag=True,
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
                                                      assigns={"SUBJECT": "*CD"},
                                                      next=Packet([Request(text="PART-OF-SPEECH is verb",
                                                                           tests={"PART-OF-SPEECH": "verb"},
                                                                           assigns={"CONCEPT": "*CD"})]))]))])

################################################################################
# Jack and Susan have a ball
lex["JACK"] = Packet([Request(text="noun JACK", test_flag=True,
                              assigns={"CD": "JACK", "PART-OF-SPEECH": "noun-phrase"})])
lex["AND"] = Packet([Request(text="conjunction AND", test_flag=True, assigns={"CD": "AND"})])
lex["SUSAN"] = Packet([Request(text="noun SUSAN", test_flag=True,
                               assigns={"CD": "SUSAN", "PART-OF-SPEECH": "noun-phrase"})])
lex["HAVE"] = Packet([Request(text="verb HAVE", test_flag=True, assigns={"CD": "HAVE", "PART-OF-SPEECH": "verb"})])
lex["A"] = Packet([Request(text="indefinite article A", test_flag=True,
                           assigns={"CD": "A", "PART-OF-SPEECH": "indefinite-article"})])
lex["BALL"] = Packet([Request(text="noun BALL", test_flag=True,
                              assigns={"CD": "BALL", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# Plants absorb water.
lex["PLANTS"] = Packet([Request(text="noun PLANTS", test_flag=True,
                                assigns={"CD": "PLANTS", "PART-OF-SPEECH": "noun-phrase"})])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]])]))])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The carbon-dioxide turns into acid.
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})])
lex["ACID"] = Packet([Request(text="noun ACID", test_flag=True,
                              assigns={"CD": "ACID", "PART-OF-SPEECH": "noun-phrase"})])
lex["TURNS"] = Packet([Request(text="verb TURNS", test_flag=True, assigns={"CD": "TURNS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])

################################################################################
# The rain falls on the soil from the cloud
lex["RAIN"] = Packet([Request(text="noun RAIN", test_flag=True,
                              assigns={"CD": "RAIN", "PART-OF-SPEECH": "noun-phrase"})])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])
lex["CLOUD"] = Packet([Request(text="noun CLOUD", test_flag=True,
                               assigns={"CD": "CLOUD", "PART-OF-SPEECH": "noun-phrase"})])
lex["FALLS"] = Packet([Request(text="verb FALLS", test_flag=True,
                               assigns={"CD": "FALLS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", "EARTH", None]],
                               next=Packet([Request(text="CD is ON",
                                                    tests={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"], ["PSTOP"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])
lex["ON"] = Packet([Request(text="prep ON", test_flag=True, assigns={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["UPDATEACT", "PTRANS", "to", "CD", None], ["ABOVE"]])]))])
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD", None]])]))])

analyzer = Analyzer(lexicon=lex)

# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
# print(analyzer.parse("plants absorb water"))
# analyzer.parse("The carbon-dioxide turns into acid.")
analyzer.parse("The rain falls on the soil from the cloud.")

# print("\n\n\n.....................................................................")
# analyzer.model.print(0)
analyzer.model.print(1)
# analyzer.model.advance_time()
analyzer.model.print(2)
# print out all time steps.

# multiple calls, keep stack
