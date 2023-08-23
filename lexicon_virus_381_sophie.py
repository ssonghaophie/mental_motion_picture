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
                                assigns={"SUBJECT":"*CD","CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT","INGEST", "container", "CD", None], ["CONTAINED"]])]))])
lex["HOST"] = Packet([Request(text="noun HOST", test_flag=True,
                               assigns={"CD": "HOST", "PART-OF-SPEECH": "noun-phrase"})])
lex["BODY"] = Packet([Request(text="noun BODY", test_flag=True,
                               assigns={"CD": "BODY", "PART-OF-SPEECH": "noun-phrase"})])


################################################################################
# The virus reaches an animal cell.
lex["REACHES"] = Packet([Request(text="verb REACHES", test_flag=True, 
                                assigns={"SUBJECT":"*CD", "CD": "REACHES", "PART-OF-SPEECH": "verb"},
                                calls=[["PTRANS", "SUBJECT", None, None]],
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
                                  assigns={"SUBJECT":"*CD", "CD": "SWALLOWS", "PART-OF-SPEECH": "verb"},
                                  calls=[["INGEST", None, "SUBJECT", None]],
                                  next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT", "INGEST", "object", "CD", None],["CONTAIN"]])]))])
            
################################################################################
# The virus' RNA is released into the cell.
# The virus releases the virus' RNA into the cell.

lex["VIRUS\'"] = Packet([Request(text="possesive VIRUS\'", test_flag=True,
                              assigns={"CD": "VIRUS", "SUBJECT": "*CD", "PART-OF-SPEECH": "noun-phrase"},
                              calls=[["INGEST", None, "CD", None]],
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase"},
                                                   calls=[["CONTAIN"], ["UPDATEACT", "INGEST", "object", "CD", None]])]))])
lex["RNA"] = Packet([Request(text="noun RNA", test_flag=True,
                              assigns={"CD": "RNA", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])
lex["IS"] = Packet([Request(text="verb IS", test_flag=True, 
                                assigns={"SUBJECT":"*CD", "CD": "IS", "PART-OF-SPEECH": "verb"})])
lex["RELEASED"] = Packet([Request(text="verb RELEASED", test_flag=True,
                               assigns={"CD": "RELEASED","PART-OF-SPEECH": "verb"},
                               calls=[["EXPEL", "SUBJECT", None, None]])])
lex["INTO"] = Packet([Request(text="prep INTO", test_flag=True,
                              assigns={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH":"noun-phrase", "EXPEL":""},
                                                    calls=[["UPDATEACT", "EXPEL","to","CD", None], ["CONTAINED"], ["INGEST", "CD", None, None]]),
                                          Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase", "INGEST":""},
                                                    calls=[["CONTAIN"], ["UPDATEACT", "INGEST", "to", "CD", None]])]))])


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
                               assigns={"SUBJECT":"*CD","CD": "RELEASES", "PART-OF-SPEECH": "verb"},
                               # change ingest, ptrans, expel to include object key 
                               calls=[["EXPEL", None, "SUBJECT", None]],
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["UPDATEACT", "EXPEL", "object", "CD", None]])],
                                                ))])
lex["NEW"] = Packet([Request(text="adjective NEW", test_flag=True,
                               assigns={"CD": "NEW", "PART-OF-SPEECH": "adj-phrase"})])
lex["VIRUSES"] = Packet([Request(text="noun VIRUSES", test_flag=True,
                               assigns={"CD": "VIRUSES", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
# The new viruses enter more cells.
lex["ENTER"] = Packet([Request(text="verb ENTER", test_flag=True, 
                                assigns={"SUBJECT":"*CD", "CD": "ENTER", "PART-OF-SPEECH": "verb"},
                                calls=[["INGEST", "SUBJECT", None, None]],
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["UPDATEACT", "INGEST", "container", "CD", None], ["CONTAINED"]])]))])
lex["MORE"] = Packet([Request(text="adjective MORE", test_flag=True,
                              assigns={"CD": "MORE", "PART-OF-SPEECH": "adjective-phrase"})])
lex["CELLS"] = Packet([Request(text="noun CELLS", test_flag=True,
                              assigns={"CD": "CELLS", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)
#analyzer.parse("A virus enters a host body. The virus reaches an animal cell. The cell swallows the virus. The virus' RNA is released into the cell. The replicated RNA and proteins form the new viruses. The animal cell releases the new viruses. The new viruses enter more cells.")
analyzer.parse("A virus enters a host body. The virus reaches an animal cell. The cell swallows the virus. The virus' RNA is released into the cell. The replicated RNA and proteins form the new viruses. The animal cell releases the new viruses. The new viruses enter more cells.")
#A virus enters a host body. The virus reaches an animal cell. The cell swallows the virus. 
# The replicated RNA and proteins form the new viruses. The animal cell releases the new viruses. The new viruses enter more cells.
#analyzer.parse("The replicated RNA and proteins form the new viruses.")
#virus expel rna (rna in virus) to cell