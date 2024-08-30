from ai.promts.jmlTransformationExampleGenerator import JmlTransformationExampleGenerator
from definitions import config
from definitions.inconsistencyTestCase import InconsistencyTestCase


class InitialPromptGenerator:
    """
    This class is responsible for generating the initial prompt that is used to generate JML.
    """

    def __init__(self, example_generator=JmlTransformationExampleGenerator()):
        self.example_generator = example_generator

    def get_initial_prompt(self, test_case: InconsistencyTestCase) -> str:
        """
        Generates the initial prompt for the JML generation.
        :param test_case: The test case that is used to generate the prompt.
        :return: The initial prompt.
        """

        return (f'Generate a JML (Java Modelling Language) for the following JavaDoc:\n {test_case.get_comment()}\n\n'
                f'The parameters for the method the comment describes are: {test_case.method_info.parameters}\n\n'
                f'Here are some examples of JavaDoc to JML transformations:\n\n'
                f'{self.get_examples()}\n\n'
                f'Only include the JML, nothing else, no code, no comments, no method name, nothing.'
                f'The JML should be surrounded by /** and */')

    def get_examples(self) -> str:
        examples = self.example_generator.get_examples(config.JML_TRANSFORMATIONS_EXAMPLES_COUNT)

        return '\n'.join([example.to_example() for example in examples])
