from absl.testing.absltest import TestCase

from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.tests.testCollection import TestCollection


class SignalTestCollection(TestCollection):
    def __init__(self, test_cases: list[TestCase], exception_type, csp_parameters: CSPParameters):
        super().__init__(test_cases, csp_parameters)
        self.exception_type = exception_type
