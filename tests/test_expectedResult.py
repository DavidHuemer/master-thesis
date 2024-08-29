from unittest import TestCase

from definitions.evaluations.expectedResult import ExpectedResult


class TestExpectedResult(TestCase):
    def test_to_string(self):
        expected_result = ExpectedResult('file_path', 'method_name', True)
        self.assertEqual(str(expected_result), 'file_path  =>  method_name=True)')

    def test_eq(self):
        expected_result1 = ExpectedResult('file_path', 'method_name', True)
        expected_result2 = ExpectedResult('file_path', 'method_name', True)
        self.assertEqual(expected_result1, expected_result2)

        expected_result3 = ExpectedResult('file_path', 'method_name', False)
        self.assertNotEqual(expected_result1, expected_result3)

        expected_result4 = ExpectedResult('file_path', 'method_name2', True)
        self.assertNotEqual(expected_result1, expected_result4)

        expected_result5 = ExpectedResult('file_path2', 'method_name', True)
        self.assertNotEqual(expected_result1, expected_result5)
