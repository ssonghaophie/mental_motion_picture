from analyzer import Request, Analyzer

# lexicon should be a hash table (python dictionary)
# key - the word
# value - definition of the word (a list of request objects)
lex = dict()
lex["*START*"] = [Request(text="start parsing",
                          test_flag=True,
                          next_packet=[Request(text="PART-OF-SPEECH is noun-phrase",
                                               tests={"PART-OF-SPEECH": "noun-phrase"},
                                               assigns={"SUBJECT": "*CD"},
                                               next_packet=[Request(text="PART-OF-SPEECH is verb",
                                                                    tests={"PART-OF-SPEECH": "verb"},
                                                                    assigns={"CONCEPT": "*CD"})])])]

################################################################################
# Jack and Susan have a ball
# lex["JACK"] = [
#     Request(text="noun JACK", test=True, test_val=None, assign_val={"PART-OF-SPEECH": "noun-phrase"}, next_packet=None)]
# lex["AND"] = [Request(text="conjunction AND", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["SUSAN"] = [Request(text="noun SUSAN", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["HAVE"] = [
#     Request(text="verb HAVE", test=True, test_val=None, assign_val={"PART-OF-SPEECH": "verb"}, next_packet=None)]
# lex["A"] = [Request(text="particle A", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["BALL"] = [Request(text="noun BALL", test=True, test_val=None, assign_val=None, next_packet=None)]

################################################################################
# Plants absorb water.
lex["PLANTS"] = [Request(text="noun PLANTS", test_flag=True, assigns={"CD": "PLANTS", "PART-OF-SPEECH": "noun-phrase"})]
lex["ABSORB"] = [Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                         next_packet=[Request(text="PART-OF-SPEECH is noun-phrase",
                                              tests={"PART-OF-SPEECH": "noun-phrase"},
                                              calls=["CONTAIN"])])]
lex["WATER"] = [Request(text="noun WATER", test_flag=True, assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})]

################################################################################
# The carbon-dioxide turns into acid.
lex["THE"] = [Request(text="definite article THE", test_flag=True, assigns={"PART-OF-SPEECH": "definite-article"})]
lex["CARBON-DIOXIDE"] = [Request(text="noun CARBON-DIOXIDE", test_flag=True,
                                 assigns={"CD": "CARBON-DIOXIDE", "PART-OF-SPEECH": "noun-phrase"})]
lex["ACID"] = [Request(text="noun ACID", test_flag=True, assigns={"CD": "ACID", "PART-OF-SPEECH": "noun-phrase"})]
lex["TURNS"] = [Request(text="verb TURNS", test_flag=True, assigns={"CD": "TURNS", "PART-OF-SPEECH": "verb"},
                        next_packet=[Request(text="PART-OF-SPEECH is noun-phrase",
                                             tests={"PART-OF-SPEECH": "noun-phrase"},
                                             calls=["STATECHANGE"])])]

################################################################################
# The rain falls on the soil
lex["RAIN"] = [Request(text="noun RAIN", test_flag=True, assigns={"CD": "RAIN", "PART-OF-SPEECH": "noun-phrase"})]
lex["SOIL"] = [Request(text="noun SOIL", test_flag=True, assigns={"CD": "SOIL", "PART-OF-SPEECH": "noun-phrase"})]
lex["FALLS"] = [Request(text="verb FALLS", test_flag=True,
                        assigns={"CD": "FALLS", "PART-OF-SPEECH": "verb"},
                        calls=["PTRANS", "EARTH", None])]  # PSTOP, advance time step
lex["ON"] = [Request(text="prep ON", test_flag=True, assigns={"CD": "ON", "PART-OF-SPEECH": "preposition"},
                     next_packet=[Request(text="PART-OF-SPEECH is noun-phrase",
                                          tests={"PART-OF-SPEECH": "noun-phrase"},
                                          calls=["ABOVE"])])]

analyzer = Analyzer(lexicon=lex)

# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
# print(analyzer.parse("plants absorb water"))
# print(analyzer.parse("The carbon-dioxide turns into acid."))
print(analyzer.parse("The rain falls on the soil."))
