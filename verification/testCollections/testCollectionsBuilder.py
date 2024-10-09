from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollections import TestCollections
from helper.logs.loggingHelper import LoggingHelper
from verification.testCollections.signalTestCollectionBuilder import SignalTestCollectionBuilder
from verification.testCollections.testCollectionBuilder import TestCollectionBuilder


class TestCollectionsBuilder:
    """
    Helper class for building TestCollections
    """

    def __init__(self, test_collection_builder=TestCollectionBuilder(),
                 signal_test_collection_builder=SignalTestCollectionBuilder()):
        self.test_collection_builder = test_collection_builder
        self.signal_test_collection_builder = signal_test_collection_builder

    def build(self, parameters: list[ParameterExtractionInfo], behavior_node: BehaviorNode) -> TestCollections:
        """
        Build TestCollections from JavaMethod and AST
        :param parameters: The parameters of the method
        :param behavior_node: The behavior node that contains the pre and post conditions
        :return: The TestCollections
        """
        LoggingHelper.log_info("Building Test Collections")

        test_collection = self.test_collection_builder.build(parameters, behavior_node.pre_conditions)
        signal_collections = self.signal_test_collection_builder.build(parameters, behavior_node.signals_conditions)
        return TestCollections(test_collection, signal_collections)
