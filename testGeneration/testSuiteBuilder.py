from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.evaluations.tests.testSuite import TestSuite
from parser.tree.astGenerator import get_ast_by_jml
from testGeneration.testCollections.testCollectionsBuilder import build_test_collections


def get_test_suite(test_case: ConsistencyTestCase, jml_code: str):
    ast = get_ast_by_jml(jml_code)

    return TestSuite(consistency_test_case=test_case,
                     behavior_tests=get_behavior_tests(ast.behavior_nodes, test_case.method_info.parameters)
                     )


def get_behavior_tests(behavior_nodes: list[BehaviorNode], parameters: list[ParameterExtractionInfo]) -> (
        list)[BehaviorTest]:
    return [get_behavior_test(behavior_node, parameters) for behavior_node in behavior_nodes]


def get_behavior_test(behavior_node: BehaviorNode, parameters: list[ParameterExtractionInfo]) -> BehaviorTest:
    test_collections = build_test_collections(parameters, behavior_node)
    return BehaviorTest(test_collections, behavior_node)
