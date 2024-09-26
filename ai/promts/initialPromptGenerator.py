from ai.promts.jmlTransformationExampleGenerator import JmlTransformationExampleGenerator
from definitions import config
from definitions.consistencyTestCase import ConsistencyTestCase


class InitialPromptGenerator:
    """
    This class is responsible for generating the initial prompt that is used to generate JML.
    """

    def __init__(self, example_generator=JmlTransformationExampleGenerator()):
        self.example_generator = example_generator

    def get_initial_prompt(self, test_case: ConsistencyTestCase) -> str:
        """
        Generates the initial prompt for the JML generation.
        :param test_case: The test case that is used to generate the prompt.
        :return: The initial prompt.
        """

        return (f'Generate a JML (Java Modelling Language) for the following JavaDoc:\n {test_case.get_comment()}\n\n'
                f'The parameters for the method the comment describes are: {test_case.method_info.parameters}\n\n'
                f'Only include the JML, nothing else, no code, no comments, no method name, nothing.\n'
                f'Do not include the name of the programming language.\n'
                f'Every line should start with the Java Comment symbol "//"\n'
                f'Do not use any external classes or methods.\n'
                f'Do not use any other classes, no static ones, nothing.\n'
                f'That means classes like Math, Arrays, etc. are not allowed.\n'
                f'Do not include any code that must be imported.\n'
                f'So for example, Math.abs is not allowed.\n'
                f'For quantified expressions (\\forall, \\exists, \\sum, \\min, ...), keep in mind, that for the '
                f'range predicate, no other predicate can be used\n'
                f'So you can write "0 <= i && i < a.length" but not: "0 <= i && i < a.length && a[i] == true".\n\n'
                f'Here are some examples of JavaDoc to JML transformations:\n\n'
                f'{self.get_examples()}')

    def get_examples(self) -> str:
        examples = self.example_generator.get_examples(config.JML_TRANSFORMATIONS_EXAMPLES_COUNT)

        return '\n'.join([example.to_example() for example in examples])
