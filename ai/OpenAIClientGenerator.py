from openai import OpenAI

from ai.tokenLoader import TokenLoader


class OpenAIClientGenerator:
    """
    Class that is responsible for generating an OpenAI client.
    """

    def __init__(self, token_loader=TokenLoader()):
        """
        Initializes the OpenAIClientGenerator.
        :param token_loader: The token loader to use.
        """
        self.token_loader = token_loader

    def generate(self):
        """
        Generates an OpenAI client.
        :return: The generated OpenAI client.
        """
        token = self.token_loader.load()
        return OpenAI(
            # This is the default and can be omitted
            api_key=token,
        )
