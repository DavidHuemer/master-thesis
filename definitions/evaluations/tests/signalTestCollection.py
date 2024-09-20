from absl.testing.absltest import TestCase

from definitions.evaluations.tests.testCollection import TestCollection


class SignalTestCollection(TestCollection):
    def __init__(self, test_cases: list[TestCase], exception_type):
        super().__init__(test_cases)
        self.exception_type = exception_type
