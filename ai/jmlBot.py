from ai.chatBot import ChatBot
from ai.openAIClient import OpenAIClient
from ai.promts.initialPromptGenerator import InitialPromptGenerator
from definitions import config
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.parser.parserError import ParserError


class JmlBot:
    def __init__(self, client: OpenAIClient, chat_bot=None, initial_prompt_generator=InitialPromptGenerator()):
        self.client = client
        self.chat_bot = ChatBot(client, config.JML_CONTEXT) if chat_bot is None else chat_bot
        self.initial_prompt_generator = initial_prompt_generator

    def get_jml(self, test_case: ConsistencyTestCase) -> str:
        initial_prompt = self.initial_prompt_generator.get_initial_prompt(test_case)
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

    def get_from_text(self, text: str):
        prompt = ("The following exception occurred:\n"
                  f"{text}\n"
                  "Please provide a new JML for the method.\n"
                  "Again, only generate the JML and nothing else, as the result is being parsed.")

        response = self.chat_bot.chat(prompt)
        return response

    def reset(self):
        self.chat_bot.reset()
