from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.verification.testCase import TestCase


class TestCollection:
    """
    Holds a collection of test cases
    """

    def __init__(self, test_cases: list[TestCase], csp_parameters: CSPParameters):
        self.test_cases = test_cases
        self.csp_parameters = csp_parameters

    def __str__(self):
        return f"TestCollection Nr of test cases: {len(self.test_cases)}"

    def get_test_cases_count(self):
        return len(self.test_cases)
