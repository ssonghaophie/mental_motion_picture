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

# find a parallel noun until a verb is encountered?
check_parallel_noun = Packet([Request(text="check parallel noun-phrases", tests={"PART-OF-SPEECH": "noun-phrase"},
                                      calls=[["UPDATEACT ADD OBJECT", "CD"]])],
                             one_time=True)

################################################################################
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])
lex["A"] = Packet([Request(text="indefinite article A", test_flag=True,
                           assigns={"CD": "A", "PART-OF-SPEECH": "indefinite-article"})])
lex["AN"] = Packet([Request(text="indefinite article AN", test_flag=True,
                           assigns={"CD": "AN", "PART-OF-SPEECH": "indefinite-article"})])

lex["AND"] = Packet([Request(text="conjunction AND", test_flag=True, assigns={"CD": "AND"},
                             next=check_parallel_noun)])


# Cells obtain glucose and oxygen.	
# The glucose and oxygen create carbon dioxide.
# The cells release energy.
### The cells don't have enough oxygen to repeat this.
# The cells obtain more oxygen from the air.
### The cells repeat this process.	
################################################################################
# Cells obtain glucose and oxygen.
# containment relationship doesn't get added when updated (only appears on INGEST primitive actions)
lex["OBTAIN"] = Packet([Request(text="verb OBTAIN", test_flag=True, assigns={"CD": "OBTAIN", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", None, "SUBJECT", None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT", "INGEST", "object", "CD", None], ["CONTAIN"]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["GLUCOSE"] = Packet([Request(text="noun GLUCOSE", test_flag=True,
                                 assigns={"CD": "GLUCOSE", "PART-OF-SPEECH": "noun-phrase"})])
lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                                 assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])
################################################################################
# The glucose and oxygen create carbon-dioxide.
lex["CREATE"] = Packet([Request(text="verb CREATE", test_flag=True, assigns={"CD": "CREATE", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["MATCH COMBO"]])]))])
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})])
################################################################################
# The cells release energy.
lex["ENERGY"] = Packet([Request(text="noun ENERGY", test_flag=True,
                                 assigns={"CD": "ENERGY", "PART-OF-SPEECH": "noun-phrase"})])
lex["RELEASE"] = Packet([Request(text="verb RELEASE", test_flag=True, assigns={"CD": "RELEASE", "PART-OF-SPEECH": "verb"},
                                 calls=[["EXPEL", None, "SUBJECT", None]],
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT", "EXPEL", "object", "CD", None]])]))])


################################################################################
# The cells obtain more oxygen from the air.
lex["CELLS"] = Packet([Request(text="noun CELLS", test_flag=True,
                              assigns={"CD": "CELLS", "PART-OF-SPEECH": "noun-phrase"})])
lex["MORE"] = Packet([Request(text="adjective MORE", test_flag=True,
                              assigns={"CD": "MORE", "PART-OF-SPEECH": "adjective-phrase"})])
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["UPDATEACT", "INGEST", "from", "CD", None]])]))])

lex["AIR"] = Packet([Request(text="noun AIR", test_flag=True,
                                 assigns={"CD": "AIR", "PART-OF-SPEECH": "noun-phrase"})])


analyzer = Analyzer(lexicon=lex)

analyzer.parse("Cells obtain glucose and oxygen. The glucose and oxygen create carbon-dioxide. The cells release energy. The cells obtain more oxygen from the air.")