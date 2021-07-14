from analyzer import Request, Analyzer

# lexicon should be a hash table (python dictionary)
# key - the word
# value - definition of the word (a list of request objects)
lex = dict()
lex["*START*"] = [Request(text="start parsing", test=True,
                          next_packet=[Request(text="part-of-speech is noun-phrase",
                                               test_val={"part-of-speech": "noun-phrase"},
                                               next_packet=[Request(text="part-of-speech is verb",
                                                                    test_val={"part-of-speech": "verb"})])])]

lex["JACK"] = [
    Request(text="noun JACK", test=True, test_val=None, assign_val={"part-of-speech": "noun-phrase"}, next_packet=None)]
lex["AND"] = [Request(text="conjunction AND", test=True, test_val=None, assign_val=None, next_packet=None)]
lex["SUSAN"] = [Request(text="noun SUSAN", test=True, test_val=None, assign_val=None, next_packet=None)]
lex["HAVE"] = [
    Request(text="verb HAVE", test=True, test_val=None, assign_val={"part-of-speech": "verb"}, next_packet=None)]
lex["A"] = [Request(text="particle A", test=True, test_val=None, assign_val=None, next_packet=None)]
lex["BALL"] = [Request(text="noun BALL", test=True, test_val=None, assign_val=None, next_packet=None)]

analyzer = Analyzer(lexicon=lex)

print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
