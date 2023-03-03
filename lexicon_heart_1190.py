# 1190 How does the heart work?

# Two large veins bring blood to the heart.
# The blood enters the right atrium.
# The blood flows through the tricuspid valve.
# The blood travels into the right ventricle.
# The blood goes through the pulmonary arteries to the lungs.
# Blood picks up oxygen in the lungs.
# Oxygenated blood enters the left atrium.
# Blood goes to the left ventricle.
# Blood leaves the heart via the aorta to the rest of the body.
# The deoxygenated blood returns to the heart.

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
# 1. Two large veins bring blood to the heart.

# 2. The blood enters the right atrium.

# 3. The blood flows through the tricuspid valve.

# 4. The blood travels into the right ventricle.

# 5. The blood goes through the pulmonary arteries to the lungs.

# 6. Blood picks up oxygen in the lungs.

# 7. Oxygenated blood enters the left atrium.

# 8. Blood goes to the left ventricle.

# 9. Blood leaves the heart via the aorta to the rest of the body.

# 10. The deoxygenated blood returns to the heart.

################################################################################
analyzer = Analyzer(lexicon=lex)

analyzer.parse("Two large veins bring blood to the heart."
               "The blood enters the right atrium."
               "The blood flows through the tricuspid valve."
               "The blood travels into the right ventricle."
               "The blood goes through the pulmonary arteries to the lungs."
               "Blood picks up oxygen in the lungs."
               "Oxygenated blood enters the left atrium."
               "Blood goes to the left ventricle."
               "Blood leaves the heart via the aorta to the rest of the body."
               "The deoxygenated blood returns to the heart.")

# directory = "~/Documents/honors/convert_to_csv"
# filename = "test_converter1_f.csv"
# converter = Converter(analyzer)
# converter.convert(filename=filename, date=True, dir=directory)
# converter.convert_propara_format(filename=filename, date=True, dir=directory)
