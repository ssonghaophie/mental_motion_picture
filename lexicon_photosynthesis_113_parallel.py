# sentences from paragraph 113 with parallel structures

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
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD", None]])]))])

# find a parallel noun until a verb is encountered?
check_parallel_noun = Packet([Request(text="check parallel noun-phrases", tests={"PART-OF-SPEECH": "noun-phrase"},
                                      calls=[["UPDATEACT ADD OBJECT", "CD"]])],
                             one_time=True)

################################################################################
# The roots absorb water and minerals from the soil.

lex["ROOTS"] = Packet([Request(text="noun ROOTS", test_flag=True,
                               assigns={"CD": "ROOTS", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]]),
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
# lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
#                               assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])

################################################################################
analyzer = Analyzer(lexicon=lex)
analyzer.parse("The roots absorb water and minerals.")
