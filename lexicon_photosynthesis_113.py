# 113
# Chloroplasts in the leaf of the plant traps light from the sun.
# The roots absorb water and minerals from the soil.
# This combination of water and minerals flows from the stem into the leaf.
# Carbon dioxide enters the leaf.
# Light, water and minerals, and the carbon dioxide all mix together.
# This mixture forms sugar (glucose) which is what the plant eats.
# Oxygen goes out of the leaf through the stomata.

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
check_parallel_noun = Packet([Request(text="check parallel noun-phrases", tests={"PART-OF-SPEECH": "noun-phrase"},
                                      calls=[["UPDATEACT ADD OBJECT", "CD"]])],
                             one_time=True)

################################################################################
# 1. Chloroplasts in the leaf of the plant traps light from the sun.
lex["CHLOROPLASTS"] = Packet([Request(text="noun CHLOROPLASTS", test_flag=True,
                                      assigns={"CD": "CHLOROPLASTS", "PART-OF-SPEECH": "noun-phrase"},
                                      next=check_parallel_noun)])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True,
                            assigns={"CD": "LEAF", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["CONTAINED"]])]))])
lex["LEAF"] = Packet([Request(text="noun LEAF", test_flag=True,
                              assigns={"CD": "LEAF", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])
lex["OF"] = Packet([Request(text="prep OF", test_flag=True,
                            assigns={"CD": "OF", "PART-OF-SPEECH": "preposition"})])
# todo: of
# part-whole relationship? at this point think of it as a containment relationship?

lex["PLANT"] = Packet([Request(text="noun PLANT", test_flag=True,
                               assigns={"CD": "PLANT", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["TRAPS"] = Packet([Request(text="verb TRAPS", test_flag=True, assigns={"CD": "TRAPS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    assigns={"OBJECT": "*CD"},
                                                    calls=[["CONTAIN"], ["INGEST"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["LIGHT"] = Packet([Request(text="noun LIGHT", test_flag=True,
                               assigns={"CD": "LIGHT", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD", None]]),
                                           Request(text="update an INGEST",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "INGEST": ""},
                                                   calls=[["UPDATEACT", "INGEST", "from", "CD", None]])]))])
lex["SUN"] = Packet([Request(text="noun SUN", test_flag=True,
                             assigns={"CD": "SUN", "PART-OF-SPEECH": "noun-phrase"},
                             next=check_parallel_noun)])

# 2. The roots absorb water and minerals from the soil.
lex["ROOTS"] = Packet([Request(text="noun ROOTS", test_flag=True,
                               assigns={"CD": "ROOTS", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAIN"], ["INGEST"]]),
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

# 3. This combination of water and minerals flows from the stem into the leaf.
lex["COMBINATION"] = Packet([Request(text="noun COMBINATION", test_flag=True,
                                     assigns={"CD": "COMBINATION", "PART-OF-SPEECH": "noun-phrase"},
                                     calls=[["MATCH COMBO"]],
                                     next=check_parallel_noun)])
lex["FLOWS"] = Packet([Request(text="verb FLOWS", test_flag=True,
                               assigns={"CD": "FLOWS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                               next=Packet([Request(text="CD is INTO",
                                                    tests={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])
lex["STEM"] = Packet([Request(text="noun STEM", test_flag=True,
                              assigns={"CD": "STEM", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])
lex["INTO"] = Packet([Request(text="prep INTO", test_flag=True, assigns={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None],
                                                          ["PSTOP"], ["CONTAINED"], ["INGESTED"]])]))])

# 4. Carbon-dioxide enters the leaf.
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"},
                                        next=check_parallel_noun)])
lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True, assigns={"CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAINED"], ["INGESTED"]])]))])

# 5. Light, water and minerals, and the carbon-dioxide all mix together.
# lex["ALL"]
lex["MIX"] = Packet([Request(text="verb MIX", test_flag=True, assigns={"CD": "MIX", "PART-OF-SPEECH": "verb"},
                             calls=[["DEFINE COMBO"]])])
# lex["TOGETHER"]
# todo: all and together have similar meanings

# 6. This mixture forms glucose which is what the plant eats.
# This mixture forms glucose.
# todo: "which"
lex["MIXTURE"] = Packet([Request(text="noun MIXTURE", test_flag=True,
                                 assigns={"CD": "MIXTURE", "PART-OF-SPEECH": "noun-phrase"},
                                 calls=[["MATCH COMBO"]])])
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True, assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["GLUCOSE"] = Packet([Request(text="noun GLUCOSE", test_flag=True,
                                 assigns={"CD": "GLUCOSE", "PART-OF-SPEECH": "noun-phrase"})])

# 7. Oxygen goes out of the leaf through the stomata.
lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                                assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])
lex["GOES"] = Packet([Request(text="verb GOES", test_flag=True,
                              assigns={"CD": "GOES", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                              next=Packet([Request(text="CD is INTO",
                                                   tests={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                                                   calls=[["ADVANCE TIME"]]),
                                           Request(text="CD is OUT",
                                                   tests={"CD": "OUT", "PART-OF-SPEECH": "preposition"})],
                                          keep=True))])
lex["OUT"] = Packet([Request(text="prep OUT", test_flag=True, assigns={"CD": "OUT", "PART-OF-SPEECH": "preposition"},
                             next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                  tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                  calls=[["UPDATEACT", "PTRANS", "from", "CD", None]])]))])
lex["THROUGH"] = Packet([Request(text="prep THROUGH", test_flag=True,
                                 assigns={"CD": "THROUGH", "PART-OF-SPEECH": "preposition"})])
lex["STOMATA"] = Packet([Request(text="noun STOMATA", test_flag=True,
                                 assigns={"CD": "STOMATA", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)

# todo: I had to remove comma manually in sentence 5?!

# analyzer.parse("Light water and minerals and carbon-dioxide all mix together. This mixture forms glucose.")
analyzer.parse("Chloroplasts in the leaf of the plant traps light from the sun. "
               "The roots absorb water and minerals from the soil. "
               "This combination of water and minerals flows from the stem into the leaf. "
               "Carbon-dioxide enters the leaf. "
               "Light water and minerals and carbon-dioxide all mix together. "
               "This mixture forms glucose. "
               "Oxygen goes out of the leaf through the stomata.")
