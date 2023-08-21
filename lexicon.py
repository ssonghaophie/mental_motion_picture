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

################################################################################
# Jack and Susan have a ball
lex["JACK"] = Packet([Request(text="noun JACK", test_flag=True,
                              assigns={"CD": "JACK", "PART-OF-SPEECH": "noun-phrase"})])
lex["SUSAN"] = Packet([Request(text="noun SUSAN", test_flag=True,
                               assigns={"CD": "SUSAN", "PART-OF-SPEECH": "noun-phrase"})])
lex["HAVE"] = Packet([Request(text="verb HAVE", test_flag=True, assigns={"CD": "HAVE", "PART-OF-SPEECH": "verb"})])
lex["BALL"] = Packet([Request(text="noun BALL", test_flag=True,
                              assigns={"CD": "BALL", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# Plants absorb water.
lex["PLANTS"] = Packet([Request(text="noun PLANTS", test_flag=True,
                                assigns={"CD": "PLANTS", "PART-OF-SPEECH": "noun-phrase"})])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"], ["INGEST"]])]))])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The carbon-dioxide turns into acid.
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

################################################################################
# The cells in the body exchange the oxygen with carbon-dioxide.
# What is the relationship? cell to another cell
lex["CELLS"] = Packet([Request(text="noun CELLS", test_flag=True,
                              assigns={"CD": "CELLS", "PART-OF-SPEECH": "noun-phrase"})])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True,
                            assigns={"OBJECT":"*CD", "CD": "IN", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     assigns={"SUBJECT": "*CD", "PART-OF-SPEECH": "preposition"},
                                                     calls=[["INGEST"], ["CONTAIN"]])]))])
lex["EXCHANGE"] = Packet([Request(text="verb EXCHANGE", test_flag=True, 
                                assigns={"CD": "EXCHANGE", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     assigns={"SUBJECT": "*CD"},
                                                     calls=[["PTRANS", "OBJECT", "OBJECT"]],
                                                        next=Packet([Request(text="CD is WITH",
                                                        tests={"PART-OF-SPEECH": "preposition"},
                                                        next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                                             tests={"PART-OF-SPEECH":"noun-phrase"},
                                                                             assigns={"SUBJECT":"*CD"},
                                                                             calls=[["PTRANS", "OBJECT", "OBJECT"]])])),
                                             Request(text="CD is WITH",
                                                     tests={"CD": "WITH", "PART-OF-SPEECH": "preposition"})]))]))])
lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                               assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])
lex["WITH"] = Packet([Request(text="prep WITH", test_flag=True,
                               assigns={"CD": "WITH", "PART-OF-SPEECH": "preposition"})])
lex["BODY"] = Packet([Request(text="noun BODY", test_flag=True,
                               assigns={"CD": "BODY", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# Put the seed in the hole.
lex["PUT"] = Packet([Request(text="verb PUT", test_flag=True, 
                                assigns={"CD": "PUT", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     assigns={"SUBJECT": "*CD"},
                                                     next=Packet([Request(text="CD is IN",
                                                     tests={"CD": "IN"},
                                                     calls=[["PSTOP"]])]))]))])
lex["SEED"] = Packet([Request(text="noun SEED", test_flag=True,
                              assigns={"CD": "SEED", "PART-OF-SPEECH": "noun-phrase"})])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True,
                            assigns={"OBJECT":"*CD", "CD": "IN", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     assigns={"SUBJECT": "*CD"},
                                                     calls=[["INGEST"], ["CONTAIN"]])]))])
lex["HOLE"] = Packet([Request(text="noun HOLE", test_flag=True,
                              assigns={"CD": "HOLE", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# Food is put into mouth.
lex["FOOD"] = Packet([Request(text="noun FOOD", test_flag=True,
                              assigns={"CD": "FOOD", "PART-OF-SPEECH": "noun-phrase"})])
lex["IS"] = Packet([Request(text="verb IS", test_flag=True, 
                                assigns={"CD": "IS", "PART-OF-SPEECH": "verb"})])
lex["MOUTH"] = Packet([Request(text="noun MOUTH", test_flag=True, 
                                assigns={"CD": "MOUTH", "PART-OF-SPEECH": "noun-phrase"})])


# A virus enters a host body.
# The virus reaches an animal cell.
# The cell swallows the virus.
# The virus' RNA is released into the cell.
# The replicated RNA and proteins form the new viruses.
# The animal cell releases the new viruses.
# The new viruses enter more cells.
################################################################################
# A virus enters a host body
lex["VIRUS"] = Packet([Request(text="noun VIRUS", test_flag=True,
                              assigns={"CD": "VIRUS", "PART-OF-SPEECH": "noun-phrase"})])
lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True, 
                                assigns={"CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["INGESTED"], ["CONTAINED"]])]))])
lex["HOST"] = Packet([Request(text="noun HOST", test_flag=True,
                               assigns={"CD": "HOST", "PART-OF-SPEECH": "noun-phrase"})])
lex["BODY"] = Packet([Request(text="noun BODY", test_flag=True,
                               assigns={"CD": "BODY", "PART-OF-SPEECH": "noun-phrase"})])


################################################################################
# The virus reaches an animal cell.
lex["REACHES"] = Packet([Request(text="verb REACHES", test_flag=True, 
                                assigns={"CD": "REACHES", "PART-OF-SPEECH": "verb"},
                                calls=[["PTRANS", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT","PTRANS", "to", "CD", None]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is TO",
                                                     tests={"CD": "TO", "PART-OF-SPEECH": "preposition"})]))])
lex["ANIMAL"] = Packet([Request(text="noun ANIMAL", test_flag=True,
                              assigns={"CD": "ANIMAL", "PART-OF-SPEECH": "noun-phrase"})])
lex["CELL"] = Packet([Request(text="noun CELL", test_flag=True,
                              assigns={"CD": "CELL", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The cell swallows the virus.
lex["SWALLOWS"] = Packet([Request(text="verb SWALLOWS", test_flag=True, 
                                assigns={"CD": "SWALLOWS", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["INGEST"],["CONTAIN"]])]))])
            
################################################################################
# The virus' RNA is released into the cell.
# The virus releases the virus' RNA into the cell.

lex["VIRUS\'"] = Packet([Request(text="possesive VIRUS\'", test_flag=True,
                              assigns={"CD": "VIRUS", "SUBJECT": "*CD", "PART-OF-SPEECH": "noun-phrase"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["CONTAIN"], ["INGEST"]])]))])
lex["RNA"] = Packet([Request(text="noun RNA", test_flag=True,
                              assigns={"CD": "RNA", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])
lex["IS"] = Packet([Request(text="verb IS", test_flag=True, 
                                assigns={"SUBJECT":"*CD", "CD": "IS", "PART-OF-SPEECH": "verb"})])
lex["RELEASED"] = Packet([Request(text="verb RELEASED", test_flag=True,
                               assigns={"CD": "RELEASED","PART-OF-SPEECH": "verb"},
                               calls=[["EXPELED", None, None]])])
lex["INTO"] = Packet([Request(text="prep INTO", test_flag=True,
                              assigns={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","to","CD", None], ["CONTAINED"], ["INGESTED"]]),
                                          Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["CONTAINED"], ["INGESTED"]])]))])


################################################################################
#The replicated RNA and proteins form the new viruses.

lex["REPLICATED"] = Packet([Request(text="adjective REPLICATED", test_flag=True,
                               assigns={"CD": "REPLICATED", "PART-OF-SPEECH": "adjective-phrase"})])
lex["PROTEINS"] = Packet([Request(text="noun PROTEINS", test_flag=True,
                               assigns={"CD": "PROTEINS", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["FORM"] = Packet([Request(text="verb FORM", test_flag=True, assigns={"CD": "FORM", "PART-OF-SPEECH": "verb"},
                              calls=[["DEFINE COMBO"]],
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["MATCH COMBO"]])]))])
lex["NEW"] = Packet([Request(text="adjective NEW", test_flag=True,
                               assigns={"CD": "NEW", "PART-OF-SPEECH": "adj-phrase"})])
lex["VIRUSES"] = Packet([Request(text="noun VIRUSES", test_flag=True,
                               assigns={"CD": "VIRUSES", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])

################################################################################
# The animal cell releases the new viruses
lex["ANIMAL"] = Packet([Request(text="noun ANIMAL", test_flag=True,
                              assigns={"CD": "ANIMAL", "PART-OF-SPEECH": "noun-phrase"})])
lex["CELL"] = Packet([Request(text="noun CELL", test_flag=True,
                              assigns={"CD": "CELL", "PART-OF-SPEECH": "noun-phrase"})])
lex["RELEASES"] = Packet([Request(text="verb RELEASES", test_flag=True,
                               assigns={"SUBJECT":"*CD", "CD": "RELEASES","PART-OF-SPEECH": "verb"},
                               calls=[["EXPEL", None, None]],
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["UPDATEACT", "EXPEL","object", "CD", None]])],
                                                ))])
lex["NEW"] = Packet([Request(text="adjective NEW", test_flag=True,
                               assigns={"CD": "NEW", "PART-OF-SPEECH": "adj-phrase"})])
lex["VIRUSES"] = Packet([Request(text="noun VIRUSES", test_flag=True,
                               assigns={"CD": "VIRUSES", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The new viruses enter more cells.
lex["ENTER"] = Packet([Request(text="verb ENTER", test_flag=True, 
                                assigns={"CD": "ENTER", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["INGESTED"], ["CONTAINED"]])]))])
lex["MORE"] = Packet([Request(text="adjective MORE", test_flag=True,
                              assigns={"CD": "MORE", "PART-OF-SPEECH": "adjective-phrase"})])
lex["CELLS"] = Packet([Request(text="noun CELLS", test_flag=True,
                              assigns={"CD": "CELLS", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)
analyzer.parse('''A virus enters a host body. The virus reaches an animal cell. 
                The cell swallows the virus. The virus' RNA is released into the cell.
                The replicated RNA and proteins form the new viruses.The animal cell releases the new viruses.
                The new viruses enter more cells.''')

# ANIMAL CELL
# HOST BODY
# all of them are two nouns -- what should I do?


# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
#print(analyzer.parse("plants absorb water"))
#analyzer.parse("The carbon-dioxide turns into acid.")
#analyzer.parse("Jack and Susan have a ball. The rain falls on the soil from the cloud.")
#analyzer.parse("Jack and Susan have a ball.")
#analyzer.parse("Jack and Susan have a ball.")

#analyzer.parse("The animal cell releases the new viruses.")
#analyzer.parse("A virus enters a host body.")
# analyzer.parse("The cells in the body exchange the oxygen with carbon-dioxide.")
#analyzer.parse("Put the seed in the hole.")
#analyzer.parse("Food is put into mouth.")

# print("\n\n\n.....................................................................")
# analyzer.model.print(0)
# analyzer.model.print(1)
# analyzer.model.advance_time()
# analyzer.model.print(2)
# print out all time steps.

# The roots absorb water and minerals from the soil.

lex["ROOTS"] = Packet([Request(text="noun ROOTS", test_flag=True,
                               assigns={"CD": "ROOTS", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["INGEST"], ["CONTAIN"]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["AND"] = Packet([Request(text="conj AND", test_flag=True,
                             assigns={"CD": "AND", "PART-OF-SPEECH": "conjunction"},
                             next=check_parallel_noun)])
lex["MINERALS"] = Packet([Request(text="noun MINERALS", test_flag=True,
                                  assigns={"CD": "MINERALS", "PART-OF-SPEECH": "noun-phrase"},
                                  next=check_parallel_noun)])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD", None]]),
                                           Request(text="update an INGEST",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "INGEST": ""},
                                                   calls=[["UPDATEACT", "INGEST", "from", "CD", None]])]))])

#analyzer.parse("The roots absorb from water and minerals from the soil.")

# TODO: release problem 
# #analyzer.parse("The virus' RNA is released into the cell.")

#analyzer.parse("The replicated RNA and proteins form the new viruses.")
#analyzer.parse("The cell replicates the virus' RNA instead of its own.")

lex["LIGHT"] = Packet([Request(text="noun LIGHT", test_flag=True,
                               assigns={"CD": "LIGHT", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["AND"] = Packet([Request(text="conj AND", test_flag=True,
                             assigns={"CD": "AND", "PART-OF-SPEECH": "conjunction"},
                             next=check_parallel_noun)])
lex["MINERALS"] = Packet([Request(text="noun MINERALS", test_flag=True,
                                  assigns={"CD": "MINERALS", "PART-OF-SPEECH": "noun-phrase"},
                                  next=check_parallel_noun)])
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"},
                                        next=check_parallel_noun)])
lex["MIX"] = Packet([Request(text="verb MIX", test_flag=True, assigns={"CD": "MIX", "PART-OF-SPEECH": "verb"},
                             calls=[["DEFINE COMBO"]])])

#analyzer.parse("Light water and minerals and carbon-dioxide all mix together.")

lex["MIXTURE"] = Packet([Request(text="noun MIXTURE", test_flag=True,
                                 assigns={"CD": "MIXTURE", "PART-OF-SPEECH": "noun-phrase"},
                                 calls=[["MATCH COMBO"]])])
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True, assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["GLUCOSE"] = Packet([Request(text="noun GLUCOSE", test_flag=True,
                                 assigns={"CD": "GLUCOSE", "PART-OF-SPEECH": "noun-phrase"})])


# analyzer.parse("This mixture forms glucose. ")

# analyzer.parse("The animal cell releases the new viruses. The new viruses enter more cells.")
# The virus reaches an animal cell.
# The virus attaches to the cell's surface.
# The cell swallows the virus.
# The virus' RNA is released into the cell.

# new primitive? - new object being created through a process (PBUILD) (PCREATE) (CREATE)
# The cell creates the new RNA?
# The cell replicates the virus' RNA instead of its own.

# The replicated RNA and proteins form the new viruses.
# The animal cell releases the new viruses.
# The new viruses enter more cells.

# multiple calls, keep stack

# Cells obtain glucose and oxygen.	
# The glucose and oxygen create carbon dioxide.
# The cells release energy.
# The cells don't have enough oxygen to repeat this.
# The cells obtain more oxygen from the air.
# The cells repeat this process.	
################################################################################
# Cells obtain glucose and oxygen.
# containment relationship doesn't get added when updated (only appears on INGEST primitive actions)
lex["OBTAIN"] = Packet([Request(text="verb OBTAIN", test_flag=True, assigns={"CD": "OBTAIN", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["INGEST"], ["CONTAIN"]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])

lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                                 assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The glucose and oxygen create carbon dioxide.
lex["CREATE"] = Packet([Request(text="verb CREATE", test_flag=True, assigns={"CD": "CREATE", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["MATCH COMBO"]])]))])
################################################################################
# The cells release energy.
lex["ENERGY"] = Packet([Request(text="noun ENERGY", test_flag=True,
                                 assigns={"CD": "ENERGY", "PART-OF-SPEECH": "noun-phrase"})])
lex["RELEASE"] = Packet([Request(text="verb RELEASE", test_flag=True, assigns={"CD": "RELEASE", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["EXPEL", "CD", None]])]))])


################################################################################
# The cells obtain more oxygen from the air.
lex["AIR"] = Packet([Request(text="noun AIR", test_flag=True,
                                 assigns={"CD": "AIR", "PART-OF-SPEECH": "noun-phrase"})])


#analyzer.parse("Cells obtain glucose and oxygen. The glucose and oxygen create carbon-dioxide. The cells release energy. The cells obtain more oxygen from the air.")

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
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAINED"], ["INGESTED"]])]))])
lex["ATMOSPHERE"] = Packet([Request(text="noun ATMOSPHERE", test_flag=True,
                                 assigns={"CD": "ATMOSPHERE", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The light reaches the oceans.
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
                                calls=[["PTRANS", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["STATECHANGE"]]),
                                             Request(text="CD is FROM",
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
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAIN"], ["INGEST"]]),
                                             Request(text="CD is IN",
                                                     tests={"CD": "IN", "PART-OF-SPEECH": "preposition"}),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True, assigns={"CD": "IN", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["INGESTED"], ["CONTAINED"]])]))])



################################################################################
# As it cools, water condenses onto particles of dust in the air.

################################################################################
# As enough water condenses, clouds are formed.
# analyzer.parse("Sunlight enters the atmosphere. The light reaches the oceans. Water vapor accumulates in the air.")
# analyzer.parse("Water evaporates to the sky.")

# merge things together and push it to github