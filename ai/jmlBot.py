from ai.chatBot import ChatBot
from ai.openAIClient import OpenAIClient
from ai.promts.initialPromptGenerator import InitialPromptGenerator
from definitions import config
from definitions.inconsistencyTestCase import InconsistencyTestCase


class JmlBot:
    def __init__(self, client: OpenAIClient, chat_bot=None, initial_prompt_generator=InitialPromptGenerator()):
        self.client = client
        self.chat_bot = ChatBot(client, config.JML_CONTEXT) if chat_bot is None else chat_bot
        self.initial_prompt_generator = initial_prompt_generator

    def get_jml(self, test_case: InconsistencyTestCase) -> str:
        initial_prompt = self.initial_prompt_generator.get_initial_prompt(test_case)
        response = self.chat_bot.chat(initial_prompt)
        return response
