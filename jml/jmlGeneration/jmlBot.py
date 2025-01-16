import os

from ai.chatBot import ChatBot
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parser.parserError import ParserError
from helper.files.fileReader import FileReader
from jml.jmlGeneration.jmlPromptGenerator import JmlPromptGenerator


class JmlBot:
    """
    Chats with the OpenAI API to generate JML (Java Modelling Language)
    """

    def __init__(self, chat_bot: ChatBot, prompt_generator: JmlPromptGenerator):
        self.chat_bot = chat_bot
        self.prompt_generator = prompt_generator
        self.chat_bot.set_context(FileReader.read(os.getenv("AI_CONTEXT_FILE")))

        # self.chat_bot = ChatBot(client, config.JML_CONTEXT) if chat_bot is None else chat_bot
        # self.initial_prompt_generator = initial_prompt_generator
        # self.ai_template_generator = ai_template_generator

    def get_jml(self, test_case: ConsistencyTestCase) -> str:
        initial_prompt = self.prompt_generator.get_initial_prompt(test_case)
        response = self.chat_bot.chat(initial_prompt)
        return response

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
        prompt = self.ai_template_generator.generate_by_exception(str(e))
        response = self.chat_bot.chat(prompt)
        return response

    def reset(self):
        self.chat_bot.reset()
