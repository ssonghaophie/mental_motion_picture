# Each word entry in the lexicon is a word packet,
# which is a list of Request objects with some flags
class Request:

    def __init__(self, text=None, test_flag=False, tests=None, assigns=None, calls=None, next=None):
        self.TEXT = text  # short explanation of the Request todo: change to lowercase
        self.TEST_FLAG = test_flag  # boolean
        self.TESTS = tests  # if all evaluations pass, set test to be True
        self.ASSIGNS = assigns  # assignments to complete if test==True
        self.CALLS = calls  # mental model function calls
        self.NEXT_PACKET = next
