import os

from definitions.consistencyTestCase import ConsistencyTestCase
from helper.files.fileReader import FileReader


class JmlPromptGenerator:
    def __init__(self):
        self.initial_prompt_template = FileReader.read(os.getenv("INITIAL_PROMPT_TEMPLATE_FILE"))

    def get_initial_prompt(self, test_case: ConsistencyTestCase) -> str:
        prompt = self.initial_prompt_template

        # TODO: Replace the placeholders in the prompt with the actual values

        return prompt
