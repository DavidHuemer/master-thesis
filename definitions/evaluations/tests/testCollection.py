from definitions.verification.testCase import TestCase


class TestCollection:
    """
    Holds a collection of test cases
    """

    def __init__(self, test_cases: list[TestCase]):
        self.test_cases = test_cases

    def __str__(self):
        return f"TestCollection Nr of test cases: {len(self.test_cases)}"
