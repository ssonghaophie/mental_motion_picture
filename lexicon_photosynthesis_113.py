# Roots absorb water from soil.
# The water flows to the leaf.
# Light from the sun and CO2 enter the leaf.
# The light, water, and CO2 combine into a mixture.
# Mixture forms sugar.

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

################################################################################
# 1. Chloroplasts in the leaf of the plant traps light from the sun.
lex["CHLOROPLASTS"] = Packet([Request(text="noun CHLOROPLASTS", test_flag=True,
                                      assigns={"CD": "CHLOROPLASTS", "PART-OF-SPEECH": "noun-phrase"})])
lex["IN"] = Packet([Request(text="prep IN", test_flag=True,
                            assigns={"CD": "LEAF", "PART-OF-SPEECH": "preposition"},
                            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                                 calls=[["CONTAINED"]])]))])
# todo: differentiate containment map and INGEST primitive acts!
lex["LEAF"] = Packet([Request(text="noun LEAF", test_flag=True,
                              assigns={"CD": "LEAF", "PART-OF-SPEECH": "noun-phrase"})])
lex["OF"] = Packet([Request(text="noun OF", test_flag=True,
                            assigns={"CD": "OF", "PART-OF-SPEECH": "preposition"})])  # todo: of
lex["PLANT"] = Packet([Request(text="noun PLANT", test_flag=True,
                               assigns={"CD": "PLANT", "PART-OF-SPEECH": "noun-phrase"})])
lex["TRAPS"] = Packet([Request(text="verb TRAPS", test_flag=True, assigns={"CD": "TRAPS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                            tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]])]))])
lex["LIGHT"] = Packet([Request(text="noun LIGHT", test_flag=True,
                               assigns={"CD": "LIGHT", "PART-OF-SPEECH": "noun-phrase"})])
lex["FROM"] = Packet([Request(text="prep FROM", test_flag=True, assigns={"CD": "FROM", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "from", "CD", None]])]))])
lex["SUN"] = Packet([Request(text="noun SUN", test_flag=True,
                             assigns={"CD": "SUN", "PART-OF-SPEECH": "noun-phrase"})])

# 2. The roots absorb water and minerals from the soil.
lex["ROOTS"] = Packet([Request(text="noun ROOTS", test_flag=True,
                               assigns={"CD": "ROOTS", "PART-OF-SPEECH": "noun-phrase"})])
lex["ABSORB"] = Packet([Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"}, calls=[["CONTAIN"]]),
                                             Request(text="CD is FROM",
                                                     tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})]))])
lex["WATER"] = Packet([Request(text="noun WATER", test_flag=True,
                               assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})])
# lex["AND"]  # todo: bring back the last verb?
lex["MINERALS"] = Packet([Request(text="noun MINERALS", test_flag=True,
                                  assigns={"CD": "MINERALS", "PART-OF-SPEECH": "noun-phrase"})])
lex["SOIL"] = Packet([Request(text="noun SOIL", test_flag=True,
                              assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})])

# 3. This combination of water and minerals flows from the stem into the leaf.
lex["COMBINATION"] = Packet([Request(text="noun COMBINATION", test_flag=True,
                                     assigns={"CD": "COMBINATION", "PART-OF-SPEECH": "noun-phrase"})])
lex["FLOWS"] = Packet([Request(text="verb FLOWS", test_flag=True,
                               assigns={"CD": "FLOWS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"], ["PSTOP"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])  # @todo advance time at the verb "flows"
lex["STEM"] = Packet([Request(text="noun STEM", test_flag=True,
                              assigns={"CD": "STEM", "PART-OF-SPEECH": "noun-phrase"})])
# lex["INTO"]

# 4. Carbon-dioxide enters the leaf.
lex["CARBON-DIOXIDE"] = Packet([Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                        assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})])
lex["ENTERS"] = Packet([Request(text="verb ENTERS", test_flag=True, assigns={"CD": "ENTERS", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["CONTAINED"]])]))])

# 5. Light, water and minerals, and the carbon-dioxide all mix together.
# lex["ALL"]
# lex["MIX"]
# lex["TOGETHER"]

# 6. This mixture forms glucose (which is what the plant eats).
lex["MIXTURE"] = Packet([Request(text="noun MIXTURE", test_flag=True,
                                 assigns={"CD": "MIXTURE", "PART-OF-SPEECH": "noun-phrase"})])
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True, assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["GLUCOSE"] = Packet([Request(text="noun GLUCOSE", test_flag=True,
                                 assigns={"CD": "GLUCOSE", "PART-OF-SPEECH": "noun-phrase"})])

# 7. Oxygen goes out of the leaf through the stomata.
lex["OXYGEN"] = Packet([Request(text="noun OXYGEN", test_flag=True,
                                assigns={"CD": "OXYGEN", "PART-OF-SPEECH": "noun-phrase"})])
# lex["GOES"]
# lex["OUT"]
# lex["THROUGH"]
lex["STOMATA"] = Packet([Request(text="noun STOMATA", test_flag=True,
                                 assigns={"CD": "STOMATA", "PART-OF-SPEECH": "noun-phrase"})])


analyzer = Analyzer(lexicon=lex)
analyzer.parse("Chloroplasts in the leaf of the plant traps light from the sun.")
# analyzer.parse("Light from the sun and CO2 enter the leaf.")
# analyzer.parse("CO2 enter the leaf.")
# analyzer.parse("Mixture forms sugar.")
