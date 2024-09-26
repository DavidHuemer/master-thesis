from unittest import TestCase
from unittest.mock import Mock

from examples.consistencyTestCaseExamples import get_consistency_test_case_example
from examples.expectedResultExamples import get_expected_result_example
from examples.javaClassExamples import get_java_code_example
from testCases.consistencyTestCaseLoader import ConsistencyTestCaseLoader


class TestConsistencyTestCaseLoader(TestCase):
    def setUp(self):
        self.expected_results_loader = Mock()
        self.java_code_loader = Mock()
        self.builder = Mock()
        self.consistency_test_case_loader = ConsistencyTestCaseLoader(self.expected_results_loader,
                                                                      self.java_code_loader, self.builder)

    def test_get_test_cases(self):
        expected_results = [get_expected_result_example()]
        self.expected_results_loader.get_expected_results.return_value = expected_results

        java_code_list = [get_java_code_example()]
        self.java_code_loader.get_java_code_from_directory.return_value = java_code_list

        test_cases = [get_consistency_test_case_example]
        self.builder.build_test_cases.return_value = test_cases

        result = self.consistency_test_case_loader.get_test_cases()
        self.assertEqual(test_cases, result)
        self.expected_results_loader.get_expected_results.assert_called_once()
        self.java_code_loader.get_java_code_from_directory.assert_called_once()
        self.builder.build_test_cases.assert_called_once_with(expected_results, java_code_list)
