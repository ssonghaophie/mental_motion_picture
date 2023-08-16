# The carbon dioxide rich blood travels to the lungs.
# The (oxygen-rich) blood travels to the lungs.
# - getting adj to work: try containment rl first

# todo: change the sentence to original!!!
################################################################################
from analyzer import Request, Packet, Analyzer
from mental_motion_picture import MentalMotionPicture


lex = dict()
lex["*START*"] = Packet([Request(text="start parsing", test_flag=True,
                                 next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                                      tests={"PART-OF-SPEECH": "noun-phrase"},
                                                      assigns={"SUBJECT": "*CD"},
                                                      next=Packet([Request(text="PART-OF-SPEECH is verb",
                                                                           tests={"PART-OF-SPEECH": "verb"},
                                                                           assigns={"CONCEPT": "*CD"})]))]))])
################################################################################
lex["THE"] = Packet([Request(text="definite article THE", test_flag=True,
                             assigns={"CD": "THE", "PART-OF-SPEECH": "definite-article"})])

lex["OXYGEN-RICH"] = Packet([
    Request(text="adjective OXYGEN-RICH", test_flag=True,
            assigns={"CD": "OXYGEN-RICH", "PART-OF-SPEECH": "adjective","SUBJECT": "OXYGEN"},
            next=Packet([Request(text="PART-OF-SPEECH is noun-phrase",
                                 tests={"PART-OF-SPEECH": "noun-phrase"},
                                 calls=[["CONTAINED"]])]))])

lex["BLOOD"] = Packet([Request(text="noun BLOOD", test_flag=True,
                               assigns={"CD": "BLOOD", "PART-OF-SPEECH": "noun-phrase"})])


lex["TRAVELS"] = Packet([Request(text="verb TRAVELS", test_flag=True,
                               assigns={"CD": "TRAVELS", "PART-OF-SPEECH": "verb"}, calls=[["PTRANS", None, None]],
                               next=Packet([Request(text="CD is TO",
                                                    tests={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                                                    calls=[["ADVANCE TIME"]]),
                                            Request(text="CD is FROM",
                                                    tests={"CD": "FROM", "PART-OF-SPEECH": "preposition"})],
                                           keep=True))])
lex["TO"] = Packet([Request(text="prep TO", test_flag=True, assigns={"CD": "TO", "PART-OF-SPEECH": "preposition"},
                              next=Packet([Request(text="update a PTRANS; PART-OF-SPEECH is noun-phrase",
                                                   tests={"PART-OF-SPEECH": "noun-phrase", "PTRANS": ""},
                                                   calls=[["UPDATEACT", "PTRANS", "to", "CD", None],
                                                          ["PSTOP"], ["CONTAINED"], ["INGESTED"]])]))])
lex["LUNGS"] = Packet([Request(text="noun LUNGS", test_flag=True,
                              assigns={"CD": "LUNGS", "PART-OF-SPEECH": "noun-phrase"})])

analyzer = Analyzer(lexicon=lex)

# print(analyzer.parse("   !!!  Jack And    susan   HAVE a baLL   !!.;  ; ... ,"))
# print(analyzer.parse("plants absorb water"))
# analyzer.parse("The carbon-dioxide turns into acid.")
# analyzer.parse("Jack and Susan have a ball. The rain falls on the soil from the cloud.")
analyzer.parse("The oxygen-rich blood travels to the lungs.")
# analyzer.parse("The rain falls on the soil from the cloud.")
# analyzer.parse("Jack and Susan have a ball.")

# print("\n\n\n.....................................................................")
# analyzer.model.print(0)
# analyzer.model.print(1)
# analyzer.model.advance_time()
# analyzer.model.print(2)
# print out all time steps.

# multiple calls, keep stack
