import os
from unittest import TestCase
from unittest.mock import Mock

from helper.files.fileFinder import FileFinder


class TestFileFinder(TestCase):

    def setUp(self):
        self.file_helper = Mock()
        self.file_finder = FileFinder(self.file_helper)
        self.test_dir = "file_finder_test_dir"

    def test_find_not_existing_folder(self):
        self.file_helper.get_directories_by_path.side_effect = FileNotFoundError

        files = self.file_finder.find(self.test_dir, "txt")
        self.assertEqual([], files)

    def test_find_no_files(self):
        self.file_helper.get_directories_by_path.return_value = []
        self.file_helper.get_files_by_path.return_value = []

        files = self.file_finder.find(self.test_dir, "txt")
        self.assertEqual([], files)

    def test_find_single_file(self):
        self.file_helper.get_directories_by_path.return_value = []
        self.file_helper.get_files_by_path.return_value = [os.path.join(self.test_dir, "test_file.txt")]

        files = self.file_finder.find(self.test_dir, "txt")
        self.assertEqual([os.path.join(self.test_dir, "test_file.txt")], files)

    def test_find_multiple_files(self):
        self.file_helper.get_directories_by_path.return_value = []
        self.file_helper.get_files_by_path.return_value = [os.path.join(self.test_dir, "test_file1.txt"),
                                                           os.path.join(self.test_dir, "test_file2.txt")]

        files = self.file_finder.find(self.test_dir, "txt")
        self.assertEqual([os.path.join(self.test_dir, "test_file1.txt"),
                          os.path.join(self.test_dir, "test_file2.txt")], files)

    def test_find_single_sub_folder(self):
        self.file_helper.get_directories_by_path.side_effect = [[os.path.join(self.test_dir, "subfolder")], []]
        self.file_helper.get_files_by_path.side_effect = [[], [os.path.join(self.test_dir, "test_file1.txt")]]

        files = self.file_finder.find(self.test_dir, "txt")
        self.assertEqual([os.path.join(self.test_dir, "test_file1.txt")], files)

    def test_incorrect_file_extension(self):
        file_name = os.path.join(self.test_dir, "test_file.txt")
        self.assertFalse(FileFinder.check_file_extension(file_name, "pdf"))

    def test_correct_file_extension(self):
        file_name = os.path.join(self.test_dir, "test_file.txt")
        self.assertTrue(FileFinder.check_file_extension(file_name, "txt"))
