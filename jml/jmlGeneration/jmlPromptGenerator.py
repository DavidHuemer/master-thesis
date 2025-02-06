import os

from ai.promts.jmlTransformationExampleGenerator import JmlTransformationExampleGenerator
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.envKeys import INITIAL_PROMPT_TEMPLATE_FILE, AI_EXAMPLES_COUNT
from helper.files.fileReader import FileReader, read_file


class JmlPromptGenerator:
    def __init__(self, example_generator=None):
        self.initial_prompt_template = read_file(os.getenv(INITIAL_PROMPT_TEMPLATE_FILE))
        self.examples_count = int(os.getenv(AI_EXAMPLES_COUNT))
        self.example_generator = example_generator or JmlTransformationExampleGenerator()

    def get_initial_prompt(self, test_case: ConsistencyTestCase) -> str:
        prompt = self.initial_prompt_template

        # TODO: Replace the placeholders in the prompt with the actual values

        # replace {javadoc} with test_case.get_comment() in the prompt
        prompt = prompt.replace("{javadoc}", test_case.get_comment())
        prompt = prompt.replace("{parameters}", str(test_case.method_info.parameters))
        prompt = prompt.replace("{examples}", self.get_examples())

        return prompt

    @staticmethod
    def get_by_exception(e: Exception) -> str:
        return (f"The following exception occurred:\n"
                f"{str(e)}\n"
                "Please provide a new JML for the method.\n"
                "Again, only generate the JML and nothing else, as the result is being parsed.")

    def get_examples(self) -> str:
        examples = self.example_generator.get_examples(self.examples_count)

        return '\n'.join([example.to_example() for example in examples])
