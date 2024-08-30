import random

from ai.promts.jmlExamplesLoader import JmlExamplesLoader


class JmlTransformationExampleGenerator(object):
    """
    Class that is used to generate JavaDoc -> JML transformation examples.
    """

    # Used for singleton pattern
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(JmlTransformationExampleGenerator, cls).__new__(cls)

        return cls.instance

    def __init__(self, examples_loader=JmlExamplesLoader()):
        """
        Instantiates a new JmlTransformationExampleGenerator
        :param examples_loader: The loader that is used to load the examples from a file.
        """
        self.examples = None
        self.examples_loader = examples_loader

    def get_examples(self, examples_count):
        """
        Gets the examples.
        :param examples_count: The number of examples to get.
        :return: A list of JML transformation examples.
        """
        if self.examples is None:
            self.examples = self.examples_loader.load()

        # If examples_count >= len(self.examples) return all examples
        if examples_count >= len(self.examples):
            return self.examples

        # Select examples_count examples from the list randomly
        return random.sample(self.examples, examples_count)
