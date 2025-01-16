from dependency_injector import containers, providers

from verification.testConstraints.testConstraintsGenerator import TestConstraintsGenerator


class TestCaseGenerationContainer(containers.DeclarativeContainer):
    test_constraint_generator = providers.Singleton(TestConstraintsGenerator)
