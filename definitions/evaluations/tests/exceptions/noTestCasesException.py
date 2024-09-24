class NoTestCasesException(Exception):
    def __init__(self):
        super().__init__("No test cases found")
