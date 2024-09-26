from unittest import TestCase

from definitions.consistencyTestCase import ConsistencyTestCase
from examples.javaClassExamples import get_java_code_example
from examples.methodExamples import get_method_example


class TestConsistencyTestCase(TestCase):
    def test_get_comment(self):
        java_code = get_java_code_example()
        method_info = get_method_example()
        expected_result = None

        consistency_test_case = ConsistencyTestCase(java_code, method_info, expected_result)
        self.assertEqual(consistency_test_case.get_comment(), method_info.comment)
