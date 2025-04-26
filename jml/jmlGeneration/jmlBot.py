import os

from ai.chatBot import ChatBot
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.envKeys import AI_CONTEXT_FILE
from definitions.parser.parserError import ParserError
from helper.files.fileReader import FileReader
from jml.jmlGeneration.jmlPromptGenerator import JmlPromptGenerator


class JmlBot:
    """
    Chats with the OpenAI API to generate JML (Java Modelling Language)
    """

    def __init__(self, chat_bot: ChatBot = None, prompt_generator: JmlPromptGenerator | None = None):
        self.chat_bot = chat_bot or ChatBot()

        # Read AI Context file
        context = FileReader.read(os.getenv(AI_CONTEXT_FILE))

        # Check if context is empty or None
        if context is None or context == "":
            raise Exception("AI Context file is empty or None.")

        self.chat_bot.set_context(context)
        self.prompt_generator = prompt_generator or JmlPromptGenerator()

    def get_jml(self, test_case: ConsistencyTestCase) -> str:
        initial_prompt = self.prompt_generator.get_initial_prompt(test_case)
        return self.chat_bot.chat(initial_prompt)

    def get_from_failing_verification(self, parameters):
        prompt = (f"The method did not succeed with the following parameters:\n{parameters}\n"
                  f"Please provide a new JML for the method.\n"
                  f"Again, only generate the JML and nothing else, as the result is being parsed.")

        response = self.chat_bot.chat(prompt)
        return response

    def get_from_parser_exception(self, parser_errors: list[ParserError]):
        prompt = ("There was an error parsing the code. The following error(s) occurred:\n"
                  f"{"\n".join([str(x) for x in parser_errors])}\n"
                  "Provide a new JML for the method.\n"
                  "Again, only generate the JML and nothing else, as the result is being parsed.")

        response = self.chat_bot.chat(prompt)
        return response

    def get_from_no_test_cases(self):
        prompt = (f"There were no test cases found for the method. "
                  f"Please provide a new JML for the method.\n"
                  f"Again, only generate the JML and nothing else, as the result is being parsed.")

        response = self.chat_bot.chat(prompt)
        return response

    def get_from_exception(self, e: Exception):
        prompt = self.prompt_generator.get_by_exception(e)
        return self.chat_bot.chat(prompt)

    def reset(self):
        self.chat_bot.reset()
