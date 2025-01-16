from unittest import TestCase
from unittest.mock import Mock

from definitions.evaluations.expectedResult import ExpectedResult
from consistencyTestCaseLoading.expectedResultsLoader import ExpectedResultsLoader


class TestExpectedResultsLoader(TestCase):

    def setUp(self):
        self.file_reader = Mock()
        self.expected_results_loader = ExpectedResultsLoader(self.file_reader)

    def test_get_expected_results_with_emtpy_file_returns_empty_array(self):
        self.file_reader.read.return_value = ''

        result = self.expected_results_loader.get_expected_results()
        self.assertEqual(result, [])

    def test_get_expected_results_with_single_line(self):
        self.file_reader.read.return_value = 'file_content'

        expected_result = ExpectedResult('java_file_path', 'method_name', True)

        self.expected_results_loader.parse_expected_result_line = (
            Mock(return_value=expected_result))

        result = self.expected_results_loader.get_expected_results()
        self.assertEqual(result, [expected_result])
        self.expected_results_loader.parse_expected_result_line.assert_called_once_with('file_content')

    def test_get_expected_results_file(self):
        file_path = 'file_path'
        self.file_reader.read.return_value = 'file_content'

        result = self.expected_results_loader.get_expected_results_file(file_path)
        self.assertEqual(result, 'file_content')
        self.file_reader.read.assert_called_with(file_path)

    def test_parse_expected_result_line(self):
        java_file_path = 'java_file_path'
        method_name = 'method_name'
        expected_result = 'true'
        line = f'{java_file_path};{method_name};{expected_result}'

        result = self.expected_results_loader.parse_expected_result_line(line)
        self.assertEqual(result.file_path, java_file_path)
        self.assertEqual(result.method_name, method_name)
        self.assertTrue(result.expected_result)

    def test_parse_expected_result_with_empty_line(self):
        line = ''
        with self.assertRaises(RuntimeError):
            self.expected_results_loader.parse_expected_result_line(line)
