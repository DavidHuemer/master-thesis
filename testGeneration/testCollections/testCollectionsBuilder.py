from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.evaluations.tests.testCollections import TestCollections
from definitions.parameters.Variables import Variables
from helper.logs.loggingHelper import log_info
from testGeneration.testCollections.signalTestCollectionBuilder import build_signal_test_collection
from testGeneration.testCollections.testCollectionBuilder import build_test_collection


def build_test_collections(variables: Variables, behavior_node: BehaviorNode) -> TestCollections:
    """
    Build TestCollections from JavaMethod and AST
    :param variables: The parameters of the method
    :param behavior_node: The behavior node that contains the pre and post conditions
    :return: The TestCollections
    """
    log_info("Building Test Collections")

    test_collection = build_test_collection(variables, behavior_node.pre_conditions)
    signal_collections = build_signal_test_collection(variables, behavior_node.signals_conditions)
    return TestCollections(test_collection, signal_collections)
