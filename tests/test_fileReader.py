import os
import shutil
from unittest import TestCase
from helper.files.fileReader import FileReader


class TestFileReader(TestCase):

    def setUp(self):
        self.test_dir = "file_reader_test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file_name = os.path.join(self.test_dir, "test_file.txt")

    def test_read(self):
        content = "Test content"
        self.create_test_file(content)

        result = FileReader.read(self.test_file_name)
        self.assertEqual(content, result)

    def test_read_not_existing_file(self):
        with self.assertRaises(FileNotFoundError):
            FileReader.read(self.test_file_name)

    def test_read_empty_file(self):
        self.create_test_file("")
        result = FileReader.read(self.test_file_name)
        self.assertEqual("", result)

    def test_multiple_lines(self):
        content = "Line 1\nLine 2\nLine 3"
        self.create_test_file(content)
        result = FileReader.read(self.test_file_name)
        self.assertEqual(content, result)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_test_file(self, content):
        with open(self.test_file_name, "w") as f:
            f.write(content)
