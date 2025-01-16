from dependency_injector import containers, providers

from jml.jmlGeneration.jmlAiGenerator import JmlAiGenerator
from jml.jmlGeneration.jmlBot import JmlBot
from jml.jmlGeneration.jmlGenerator import JmlGenerator
from jml.jmlGeneration.jmlPromptGenerator import JmlPromptGenerator
from jml.jmlGeneration.jmlProvider import JmlProvider


# from jml.jmlProvider import JmlProvider
# from jml.jmlGenerator import JmlGenerator


class JmlIOContainer(containers.DeclarativeContainer):
    chat_bot = providers.Dependency()

    prompt_generator = providers.Factory(
        JmlPromptGenerator
    )

    jml_bot = providers.Factory(
        JmlBot,
        chat_bot=chat_bot,
        prompt_generator=prompt_generator
    )

    jml_ai_generator = providers.Factory(
        JmlAiGenerator,
        jml_bot=jml_bot
    )

    jml_generator = providers.Factory(
        JmlGenerator,
        jml_ai_generator=jml_ai_generator
    )

    jml_provider = providers.Factory(
        JmlProvider,
        jml_generator=jml_generator
    )
