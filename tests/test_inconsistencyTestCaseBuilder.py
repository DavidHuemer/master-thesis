from unittest import TestCase
from unittest.mock import Mock

from definitions.consistencyTestCase import ConsistencyTestCase
from examples.expectedResultExamples import get_expected_result_example
from examples.javaClassExamples import get_java_code_example
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder


class TestConsistencyTestCaseBuilder(TestCase):
    def setUp(self):
        self.expected_result_finder = Mock()
        self.inconsistency_test_case_builder = ConsistencyTestCaseBuilder(self.expected_result_finder)

    def test_build_test_cases_with_empty_arrays(self):
        expected_results = []
        java_code_list = []

        inconsistency_test_cases = self.inconsistency_test_case_builder.build_test_cases(expected_results,
                                                                                         java_code_list)
        self.assertEqual(inconsistency_test_cases, [])

    def test_build_with_only_expected_results(self):
        expected_results = [get_expected_result_example()]
        java_code_list = []

        inconsistency_test_cases = self.inconsistency_test_case_builder.build_test_cases(expected_results,
                                                                                         java_code_list)
        self.assertEqual(inconsistency_test_cases, [])

    def test_build_with_only_java_code(self):
        expected_results = []

        java_code = get_java_code_example()
        java_code_list = [java_code]

        self.inconsistency_test_case_builder.build_test_case = Mock()
        expected_test_case = ConsistencyTestCase(java_code, java_code.methods[0], None)
        self.inconsistency_test_case_builder.build_test_case.return_value = expected_test_case

        inconsistency_test_cases = self.inconsistency_test_case_builder.build_test_cases(expected_results,
                                                                                         java_code_list)
        self.assertEqual(inconsistency_test_cases, [expected_test_case])
        self.inconsistency_test_case_builder.build_test_case.assert_called_once_with(java_code, java_code.methods[0],
                                                                                     expected_results)

    def test_build_test_case_with_no_expected_results(self):
        java_code = get_java_code_example()
        method = java_code.methods[0]
        expected_results = []

        self.expected_result_finder.get_expected_result_for_code.return_value = None
        inconsistency_test_case = self.inconsistency_test_case_builder.build_test_case(java_code, method,
                                                                                       expected_results)
        self.assertEqual(inconsistency_test_case, ConsistencyTestCase(java_code, method, None))
        self.expected_result_finder.get_expected_result_for_code.assert_called_once_with(java_code, method,
                                                                                         expected_results)

    def test_build_test_case_with_expected_results(self):
        java_code = get_java_code_example()
        method = java_code.methods[0]
        expected_results = [get_expected_result_example()]

        self.expected_result_finder.get_expected_result_for_code.return_value = expected_results[0]
        inconsistency_test_case = self.inconsistency_test_case_builder.build_test_case(java_code, method,
                                                                                       expected_results)
        self.assertEqual(inconsistency_test_case, ConsistencyTestCase(java_code, method, expected_results[0]))
        self.expected_result_finder.get_expected_result_for_code.assert_called_once_with(java_code, method,
                                                                                         expected_results)

    # def test_build_test_case(self):
    #     self.fail()
