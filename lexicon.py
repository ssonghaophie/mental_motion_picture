from analyzer import Request, Analyzer
from map import Containment, Space, Touching
from mental_model import Time_step, Mental_model

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

# lex["JACK"] = [
#     Request(text="noun JACK", test=True, test_val=None, assign_val={"PART-OF-SPEECH": "noun-phrase"}, next_packet=None)]
# lex["AND"] = [Request(text="conjunction AND", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["SUSAN"] = [Request(text="noun SUSAN", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["HAVE"] = [
#     Request(text="verb HAVE", test=True, test_val=None, assign_val={"PART-OF-SPEECH": "verb"}, next_packet=None)]
# lex["A"] = [Request(text="particle A", test=True, test_val=None, assign_val=None, next_packet=None)]
# lex["BALL"] = [Request(text="noun BALL", test=True, test_val=None, assign_val=None, next_packet=None)]

lex["PLANTS"] = [Request(text="noun PLANTS", test_flag=True, assigns={"CD": "PLANTS", "PART-OF-SPEECH": "noun-phrase"})]
lex["ABSORB"] = [Request(text="verb ABSORB", test_flag=True, assigns={"CD": "ABSORB", "PART-OF-SPEECH": "verb"},
                         next_packet=[Request(text="PART-OF-SPEECH is noun-phrase",
                                              tests={"PART-OF-SPEECH": "noun-phrase"},
                                              calls="CONTAIN")])]
lex["WATER"] = [Request(text="noun WATER", test_flag=True, assigns={"CD": "WATER", "PART-OF-SPEECH": "noun-phrase"})]

analyzer = Analyzer(lexicon=lex)

# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
print(analyzer.parse("plants absorb water"))
