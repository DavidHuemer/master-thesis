from dependency_injector import containers, providers

from testGeneration.constraints.expressionConstraintBuilder import ExpressionConstraintBuilder


class ConstraintsContainer(containers.DeclarativeContainer):
    expression_constraint_builder = providers.Singleton(
        ExpressionConstraintBuilder
    )
