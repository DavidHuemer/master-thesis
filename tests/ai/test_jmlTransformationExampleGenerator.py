from unittest import TestCase
from unittest.mock import Mock

from ai.promts.jmlTransformationExampleGenerator import JmlTransformationExampleGenerator
from definitions.ai.jmlTransormationExample import JmlTransformationExample


class TestJmlTransformationExampleGenerator(TestCase):
    def setUp(self):
        self.examples_loader = Mock()
        self.jmlTransformationExampleGenerator = JmlTransformationExampleGenerator(self.examples_loader)

    def test_get_examples_with_no_existing_examples(self):
        self.examples_loader.load.return_value = []
        self.assertEqual([], self.jmlTransformationExampleGenerator.get_examples(1))

    def test_get_examples_with_existing_examples(self):
        examples = [
            JmlTransformationExample('A', 'B'),
            JmlTransformationExample('C', 'D'),
            JmlTransformationExample('E', 'F'),
        ]

        self.examples_loader.load.return_value = examples
        self.assertEqual(examples, self.jmlTransformationExampleGenerator.get_examples(3))

    def test_get_examples_with_random_examples(self):
        examples = [
            JmlTransformationExample('A', 'B'),
            JmlTransformationExample('C', 'D'),
            JmlTransformationExample('E', 'F'),
        ]

        self.examples_loader.load.return_value = examples
        self.assertEqual(2, len(self.jmlTransformationExampleGenerator.get_examples(2)))
