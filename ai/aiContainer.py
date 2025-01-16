from dependency_injector import containers, providers
from openai import OpenAI

from ai.chatBot import ChatBot
from ai.openAIClient import OpenAIClient
from definitions import config
from helper.files.fileReader import FileReader


class AiContainer(containers.DeclarativeContainer):
    client = providers.Resource(
        OpenAI,
        api_key=FileReader.read(config.API_KEY_PATH)
    )

    open_ai_client = providers.Resource(
        OpenAIClient,
        client=client
    )

    chat_bot = providers.Factory(
        ChatBot,
        client=open_ai_client
    )
