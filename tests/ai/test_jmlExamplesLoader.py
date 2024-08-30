from unittest import TestCase
from unittest.mock import Mock

from ai.promts.jmlExamplesLoader import JmlExamplesLoader
from definitions.ai.jmlTransormationExample import JmlTransformationExample


class TestJmlExamplesLoader(TestCase):
    def setUp(self):
        self.file_reader = Mock()
        self.jml_examples_loader = JmlExamplesLoader(self.file_reader)

    def test_load_empty_file(self):
        self.file_reader.read.return_value = ''
        result = self.jml_examples_loader.load()
        self.assertEqual(result, [])

    def test_load_file_with_invalid_content(self):
        self.file_reader.read.return_value = 'invalid content'
        result = self.jml_examples_loader.load()
        self.assertEqual(result, [])

    def test_load_file_with_one_example(self):
        self.file_reader.read.return_value = 'A\n-----\nB'
        result = self.jml_examples_loader.load()
        self.assertEqual(result, [JmlTransformationExample('A', 'B')])

    def test_load_file_with_two_examples(self):
        self.file_reader.read.return_value = 'A\n-----\nB\n=====\nC\n-----\nD'
        result = self.jml_examples_loader.load()
        self.assertEqual(result, [JmlTransformationExample('A', 'B'), JmlTransformationExample('C', 'D')])
