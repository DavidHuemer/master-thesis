from absl.testing.absltest import TestCase

from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.tests.testCollection import TestCollection
from definitions.parameters.Variables import Variables


class SignalTestCollection(TestCollection):
    def __init__(self, test_cases: list[Variables], exception_type):
        super().__init__(test_cases)
        self.exception_type = exception_type
