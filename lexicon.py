from analyzer import Request, Analyzer
from mental_model import Mental_model, Time_step
from map import Containment, Touching, Space

# lexicon should be a hash table (python dictionary)
# key - the word
# value - definition of the word (a list of request objects)
lex = {}
lex["JACK"] = [Request(test=True, text="noun JACK", assign=None, next_packet=None)]
lex["AND"] = [Request(test=True, text="conjunction AND", assign=None, next_packet=None)]
lex["SUSAN"] = [Request(test=True, text="noun SUSAN", assign=None, next_packet=None)]
lex["HAVE"] = [Request(test=True, text="verb HAVE", assign=None, next_packet=None)]
lex["A"] = [Request(test=True, text="particle A", assign=None, next_packet=None)]
lex["BALL"] = [Request(test=True, text="noun BALL", assign=None, next_packet=None)]

analyzer = Analyzer(lexicon=lex)

print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
# print(analyzer.SENTENCE)
