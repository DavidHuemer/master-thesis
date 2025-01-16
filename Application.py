from dependency_injector import containers, providers
from dependency_injector.providers import Container

from ai.aiContainer import AiContainer
from jml.jmlGeneration.containers import JmlIOContainer
from parser.parserContainer import ParserContainer
from pipeline.containers import PipelineContainer
from testGeneration.constraints.constraintsContainer import ConstraintsContainer
from testGeneration.testCaseGeneration.testCaseGenerationContainer import TestCaseGenerationContainer


class Application(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    ai: Container[AiContainer] = providers.Container(
        AiContainer
    )

    jml = providers.Container(
        JmlIOContainer,
        chat_bot=ai.chat_bot
    )

    pipeline = providers.Container(
        PipelineContainer,
        jml_provider=jml.jml_provider
    )

    parser = providers.Container(
        ParserContainer
    )

    constraints = providers.Container(
        ConstraintsContainer
    )

    test_case_generation = providers.Container(
        TestCaseGenerationContainer
    )

    # test_cases: Container[ConsistencyTestCaseContainers] = providers.Container(
    #     ConsistencyTestCaseContainers,
    # )
    #
    # code_execution = providers.Container(
    #     CodeExecutionContainers
    # )
    #
    # pipeline: Container[PipelineContainers] = providers.Container(
    #     PipelineContainers,
    #     test_case_loader=test_cases.test_case_loader,
    #     vm_helper=code_execution.vm.vm
    # )
    #
    # jml = providers.Container(
    #     JmlIOContainer,
    #     config=config
    # )
