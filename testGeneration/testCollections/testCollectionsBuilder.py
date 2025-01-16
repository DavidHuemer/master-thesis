from codetiming import Timer

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollections import TestCollections
from helper.logs.loggingHelper import log_info
from testGeneration.testCollections.signalTestCollectionBuilder import build_signal_test_collection
from testGeneration.testCollections.testCollectionBuilder import build_test_collection

test_collections_build_timer = Timer(name="build_test_collections", logger=None)


@test_collections_build_timer
def build_test_collections(parameters: list[ParameterExtractionInfo], behavior_node: BehaviorNode) -> TestCollections:
    """
    Build TestCollections from JavaMethod and AST
    :param parameters: The parameters of the method
    :param behavior_node: The behavior node that contains the pre and post conditions
    :return: The TestCollections
    """

    log_info("Building Test Collections")

    test_collection = build_test_collection(parameters, behavior_node.pre_conditions)
    signal_collections = build_signal_test_collection(parameters, behavior_node.signals_conditions)
    return TestCollections(test_collection, signal_collections)
