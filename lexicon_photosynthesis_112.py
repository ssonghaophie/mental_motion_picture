# 112
# Carbon dioxide enters the leaf through the stomates.
# Water is absorbed by the plant and transported to the leaves.
# Sunlight is captured by the plant.
# Energy in the form of ATP is made from the sun's energy.
# Carbon dioxide, water, and ATP form sugars via the Calvin cycle.
# Oxygen is given off as a byproduct.
# Oxygen leaves the leaf through the stomates.
# Water is reused or it leaves the leaf.
# The sugars can be used by the plant to make cellulose.

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
