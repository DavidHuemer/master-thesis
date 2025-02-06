import os

from openai import OpenAI

from definitions import config
from definitions.ai.openAIMessage import OpenAIMessage
from definitions.envKeys import OPEN_AI_MODEL
from helper.files.fileReader import read_file


class OpenAIClient:
    """
    Wrapper class for the OpenAI API.
    """

    def __init__(self, client=None):
        """
        Initializes the OpenAIClient with the given client.
        :param client: The actual OpenAI client.
        """

        if client is None:
            client = OpenAI(api_key=read_file(config.API_KEY_PATH))
            print("Initialized OpenAI client.")

        self.client = client
        self.model = os.getenv(OPEN_AI_MODEL)

    def get_response(self, messages: list[OpenAIMessage]):
        """
        Gets a response from the OpenAI API.
        :param messages: The messages to send to the API.
        :return: The response from the API.
        """
        return self.client.chat.completions.create(
            messages=[message.get_json() for message in messages],
            model=self.model,
        )
