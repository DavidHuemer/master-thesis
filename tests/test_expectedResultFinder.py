from unittest import TestCase

from examples.expectedResultExamples import get_expected_result_example
from examples.javaClassExamples import get_java_code_example
from examples.methodExamples import get_method_example
from consistencyTestCaseLoading.expectedResultFinder import ExpectedResultFinder


class TestExpectedResultFinder(TestCase):

    def test_get_expected_result_for_code_with_empty_expected_results(self):
        expected_result = (ExpectedResultFinder
                           .get_expected_result_for_code(get_java_code_example(),
                                                         get_method_example(),
                                                         []))

        self.assertIsNone(expected_result)

    def test_get_expected_result_for_code_with_no_matching_expected_result(self):
        expected_result = (ExpectedResultFinder
                           .get_expected_result_for_code(get_java_code_example(),
                                                         get_method_example(),
                                                         [get_expected_result_example(file_path="not_existing")]))

        self.assertIsNone(expected_result)

    def test_get_expected_result_for_code_with_matching_expected_result(self):
        path = "path"
        name = "method_name"
        expected_result = get_expected_result_example(file_path=path,
                                                      method_name=name)

        result = (ExpectedResultFinder
                  .get_expected_result_for_code(get_java_code_example(file_path=path),
                                                get_method_example(name=name),
                                                [expected_result]))

        self.assertEqual(expected_result, result)
