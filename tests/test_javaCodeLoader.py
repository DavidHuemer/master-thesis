from unittest import TestCase
from unittest.mock import Mock

from codeLoading.javaCodeLoader import JavaCodeLoader
from examples.javaClassExamples import get_java_code_example


class TestJavaCodeLoader(TestCase):
    def setUp(self):
        self.java_code_finder = Mock()
        self.java_code_reader = Mock()
        self.java_code_loder = JavaCodeLoader(self.java_code_finder, self.java_code_reader)

    def test_get_java_code_from_directory(self):
        java_code_list = [get_java_code_example()]

        self.java_code_loder.get_java_code_from_files = Mock()
        self.java_code_finder.get_java_file_paths_from_directory.return_value = ["file1", "file2"]
        self.java_code_loder.get_java_code_from_files.return_value = java_code_list

        result = self.java_code_loder.get_java_code_from_directory("directory")

        self.assertEqual(result, java_code_list)
        self.java_code_finder.get_java_file_paths_from_directory.assert_called_once_with("directory")
        self.java_code_loder.get_java_code_from_files.assert_called_once_with(["file1", "file2"])

    def test_get_java_code_from_files_with_empty_array(self):
        result = self.java_code_loder.get_java_code_from_files([])

        self.assertEqual(result, [])

    def test_get_java_code_from_files_with_one_file(self):
        java_code = get_java_code_example()

        self.java_code_reader.get_java_from_file.return_value = java_code

        result = self.java_code_loder.get_java_code_from_files(["file1"])

        self.assertEqual(result, [java_code])
        self.java_code_reader.get_java_from_file.assert_called_once_with("file1")

    def test_get_java_code_from_files_with_multiple_files(self):
        java_code1 = get_java_code_example()
        java_code2 = get_java_code_example()

        self.java_code_reader.get_java_from_file.side_effect = [java_code1, java_code2]

        result = self.java_code_loder.get_java_code_from_files(["file1", "file2"])

        self.assertEqual(result, [java_code1, java_code2])
        self.java_code_reader.get_java_from_file.assert_any_call("file1")
        self.java_code_reader.get_java_from_file.assert_any_call("file2")
        self.assertEqual(self.java_code_reader.get_java_from_file.call_count, 2)

    def test_get_java_code_from_files_with_error(self):
        self.java_code_reader.get_java_from_file.side_effect = Exception("Error")

        result = self.java_code_loder.get_java_code_from_files(["file1"])

        self.assertEqual(result, [])
        self.java_code_reader.get_java_from_file.assert_called_once_with("file1")
        self.assertEqual(self.java_code_reader.get_java_from_file.call_count, 1)