from analyzer import Request, Analyzer
from mental_model import Mental_model, Time_step
from map import Containment, Touching, Space

# lexicon should be a hash table (python dictionary)
# key - the word
# value - definition of the word (a list of request objects)
lex = {}
lex["JACK"] = [Request(test=True, assign=None, next_packet=None)]

analyzer = Analyzer(lexicon=lex)

print(analyzer.parse("   !!!  Jack susan   HAVE a baLL   !!.;  ; ... ,"))
