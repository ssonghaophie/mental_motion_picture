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


# 720
# Sunlight enters the atmosphere.
# The light reaches the oceans.
# The oceans are warmed.
# Water evaporates.
# Water vapor accumulates in the air.
# As it cools, water condenses onto particles of dust in the air.
# As enough water condenses, clouds are formed.
################################################################################
# Sunlight enters the atmosphere.
lex["SUNLIGHT"] = Packet([Request(text="noun SUNLIGHT", test_flag=True,
                                 assigns={"CD": "SUNLIGHT", "PART-OF-SPEECH": "noun-phrase"})])
lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True, assigns={"CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT", "INGEST", "container","CD", None], ["CONTAINED"]])]))])
lex["ATMOSPHERE"] = Packet([Request(text="noun ATMOSPHERE", test_flag=True,
                                 assigns={"CD": "ATMOSPHERE", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The light reaches the oceans.
lex["LIGHT"] = Packet([Request(text="noun LIGHT", test_flag=True,
                               assigns={"CD": "LIGHT", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["REACHES"] = Packet([Request(text="verb REACHES", test_flag=True, 
                                assigns={"CD": "REACHES", "PART-OF-SPEECH": "verb"},
                                calls=[["PTRANS", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT","PTRANS", "to", "CD", None]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is TO",
                                                     tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])
lex["OCEANS"] = Packet([Request(text="noun OCEANS", test_flag=True,
                                 assigns={"CD": "OCEANS", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The oceans are warmed.

################################################################################
# Water evaporates to the sky.
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                                 assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"},
                                 next=Packet([Request(text="CD is EVAPORATES",
                                                     tests={"CD": "EVAPORATES"},
                                                     assigns={"CD": "VAPOR"},
                                                     calls=[["STATECHANGE"]])]))])
lex["EVAPORATES"] = Packet([Request(text="verb EVAPORATES", test_flag=True, 
                                assigns={"CD": "EVAPORATES", "PART-OF-SPEECH": "verb"},
                                calls=[["PTRANS", "SUBJECT", None, None], ["STATECHANGE", "SUBJECT", "VAPOR"]],
                                next=Packet([Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is TO",
                                                     tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])
lex["TO"] = Packet([Request(text="prep TO", test_flag=True, assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None]]),
                                           Request(text="update an INGEST",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "INGEST": ""},
                                                   calls=[["UPDATEACT", "INGEST", "to", "CD", None]])]))])

lex["SKY"] = Packet([Request(text="noun SKY", test_flag=True,
                                 assigns={"CD": "SKY", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# Water vapor accumulates in the air.
lex["VAPOR"] = Packet([Request(text="noun VAPOR", test_flag=True,
                                 assigns={"CD": "VAPOR", "PART-OF-SPEECH": "noun-phrase"})])
lex["ACCUMULATES"] = Packet([Request(text="verb ACCUMULATES", test_flag=True, 
                                assigns={"CD": "ACCUMULATES", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAIN"]]),
                                             Request(text="CD is IN",
                                                     tests={"CD": "IN", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True, assigns={"CD": "IN", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["UPDATEACT","INGEST", "container", "CD", None], ["CONTAINED"]])]))])
lex["AIR"] = Packet([Request(text="noun AIR", test_flag=True,
                                 assigns={"CD": "AIR", "PART-OF-SPEECH": "noun-phrase"})])



################################################################################
# As it cools, water condenses onto particles of dust in the air.

################################################################################
# As enough water condenses, clouds are formed.

analyzer = Analyzer(lexicon=lex)
analyzer.parse("Sunlight enters the atmosphere. Sunlight reaches the oceans. Water vapor accumulates in the air.")
# analyzer.parse("Water evaporates to the sky.")