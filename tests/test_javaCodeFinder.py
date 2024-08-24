from unittest import TestCase
from unittest.mock import Mock

from codeLoading.javaCodeFinder import JavaCodeFinder


class TestJavaCodeFinder(TestCase):
    def setUp(self):
        self.file_finder = Mock()
        self.java_code_finder = JavaCodeFinder(file_finder=self.file_finder)

    def test_get_java_file_paths_from_directory_returns_correct_value(self):
        self.file_finder.find.return_value = ["file1.java", "file2.java", "file3.java"]

        result = self.java_code_finder.get_java_file_paths_from_directory("directory")
        self.assertEqual(result, ["file1.java", "file2.java", "file3.java"])

    def test_get_java_file_paths_from_directory_calls_file_finder_with_correct_parameters(self):
        self.java_code_finder.get_java_file_paths_from_directory("directory")
        self.file_finder.find.assert_called_once_with("directory", "java")
