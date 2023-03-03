# 221 How are clouds formed?

# Warm air rises.
# Then it expands and cools.
# Some of the vapor condenses onto tiny pieces of dust that are floating in the air.
# Forms a tiny droplet around each dust particle.
# Billions of these droplets come together they become a visible cloud.

################################################################################
from analyzer import Request, Packet, Analyzer
from converter import Converter

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
lex["AND"] = Packet([Request(text="conj AND", test_flag=True,
                             assigns={"CD": "AND", "PART-OF-SPEECH": "conjunction"},
                             next=check_parallel_noun)])

################################################################################
# 1. Warm air rises.
lex["WARM"] = Packet([Request(text="adjective WARM", test_flag=True,
                              assigns={"CD": "WARM", "PART-OF-SPEECH": "adjective"})])
lex["AIR"] = Packet([Request(text="noun AIR", test_flag=True,
                             assigns={"CD": "AIR", "PART-OF-SPEECH": "noun-phrase"},
                             next=check_parallel_noun)])
lex["RISES"] = Packet([Request(text="verb RISES", test_flag=True,
                               assigns={"CD": "RISES", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                               next=Packet([Request(text="CD is INTO",
                                                    tests={"CD": "INTO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])

# 2. Then it expands and cools.
lex["IT"] = Packet([Request(text="noun IT", test_flag=True,
                            assigns={"CD": "IT", "PART-OF-SPEECH": "noun-phrase"},
                            next=check_parallel_noun)])
lex["EXPANDS"] = Packet([Request(text="verb EXPANDS", test_flag=True,
                                 assigns={"CD": "EXPANDS", "PART-OF-SPEECH": "verb"})])
lex["COOLS"] = Packet([Request(text="verb COOLS", test_flag=True,
                               assigns={"CD": "COOLS", "PART-OF-SPEECH": "verb"})])

# 3. Some of the vapor condenses onto tiny pieces of dust that are floating in the air.
# todo: pieces of dust
lex["VAPOR"] = Packet([Request(text="noun VAPOR", test_flag=True,
                               assigns={"CD": "VAPOR", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])
lex["CONDENSES"] = Packet([Request(text="verb CONDENSES", test_flag=True,
                                   assigns={"CD": "CONDENSES", "PART-OF-SPEECH": "verb"})])

lex["PIECES"] = Packet([Request(text="noun PIECES", test_flag=True,
                                assigns={"CD": "PIECES", "PART-OF-SPEECH": "noun-phrase"},
                                next=check_parallel_noun)])
lex["DUST"] = Packet([Request(text="noun DUST", test_flag=True,
                              assigns={"CD": "DUST", "PART-OF-SPEECH": "noun-phrase"},
                              next=check_parallel_noun)])

# 4. Forms a tiny droplet around each dust particle.
lex["FORMS"] = Packet([Request(text="verb FORMS", test_flag=True, assigns={"CD": "FORMS", "PART-OF-SPEECH": "verb"},
                               next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                    tests={"PART-OF-SPEECH": "noun-phrase"},
                                                    calls=[["STATECHANGE"]])]))])
lex["DROPLET"] = Packet([Request(text="noun DROPLET", test_flag=True,
                                 assigns={"CD": "DROPLET", "PART-OF-SPEECH": "noun-phrase"},
                                 next=check_parallel_noun)])
lex["PARTICLE"] = Packet([Request(text="noun PARTICLE", test_flag=True,
                                  assigns={"CD": "PARTICLE", "PART-OF-SPEECH": "noun-phrase"},
                                  next=check_parallel_noun)])

# 5. Billions of these droplets come together they become a visible cloud.
# todo: billions
# todo: droplet ~ droplets
lex["DROPLETS"] = Packet([Request(text="noun DROPLETS", test_flag=True,
                                  assigns={"CD": "DROPLETS", "PART-OF-SPEECH": "noun-phrase"},
                                  next=check_parallel_noun)])
lex["BECOME"] = Packet([Request(text="verb BECOME", test_flag=True, assigns={"CD": "BECOME", "PART-OF-SPEECH": "verb"},
                                next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                     tests={"PART-OF-SPEECH": "noun-phrase"},
                                                     calls=[["STATECHANGE"]])]))])
lex["CLOUD"] = Packet([Request(text="noun CLOUD", test_flag=True,
                               assigns={"CD": "CLOUD", "PART-OF-SPEECH": "noun-phrase"},
                               next=check_parallel_noun)])

################################################################################
analyzer = Analyzer(lexicon=lex)

analyzer.parse("Warm air rises. "
               "Then it expands and cools. "
               "Some of the vapor condenses onto tiny pieces of dust that are floating in the air. "
               "Forms a tiny droplet around each dust particle. "
               "Billions of these droplets come together they become a visible cloud.")

# directory = "~/Documents/honors/convert_to_csv"
# filename = "test_converter1_f.csv"
# converter = Converter(analyzer)
# converter.convert(filename=filename, date=True, dir=directory)
# converter.convert_propara_format(filename=filename, date=True, dir=directory)
