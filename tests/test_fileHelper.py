import os
import shutil
from unittest import TestCase

from helper.files.fileHelper import FileHelper


class TestFileHelper(TestCase):

    def setUp(self):
        # Create a test directory
        self.test_dir = "test_directory"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a test file
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("Test content")

    def test_get_directories_by_path_returns_correct_directories(self):
        # create three subdirectories: test-1, test-2, test-3
        for i in range(1, 4):
            os.makedirs(os.path.join(self.test_dir, f"test-{i}"), exist_ok=True)

        # get all directories in the test directory
        directories = FileHelper.get_directories_by_path(self.test_dir)

        # check if the directories are correct
        self.assertEqual(directories, [os.path.join(self.test_dir, f"test-{i}") for i in range(1, 4)])

    def test_get_directories_by_path_with_empty_directory(self):
        # get all directories in the test directory
        directories = FileHelper.get_directories_by_path(self.test_dir)

        # check if the directories are correct
        self.assertEqual(directories, [])

    def test_get_files_by_path_returns_file(self):
        os.makedirs(os.path.join(self.test_dir, f"subfolder"), exist_ok=True)
        files = FileHelper.get_files_by_path(self.test_dir)

        self.assertEqual(files, [os.path.join(self.test_dir, "test_file.txt")])

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
