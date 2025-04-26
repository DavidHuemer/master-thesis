from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.parameters.Variables import Variables
from helper.parameterHelper.parameterGenerator import get_initial_parameter
from parser.tree.astGenerator import get_ast_by_jml
from testGeneration.testCollections.testCollectionsBuilder import build_test_collections


def get_test_suite(test_case: ConsistencyTestCase, jml_code: str) -> TestSuite:
    ast = get_ast_by_jml(jml_code)

    variables = Variables()

    for param in test_case.method_info.parameters:
        variables.add_method_call_parameter(get_initial_parameter(param.variable_type, param.name, param.dimension))

    return TestSuite(consistency_test_case=test_case,
                     behavior_tests=get_behavior_tests(ast.behavior_nodes, variables)
                     )


def get_behavior_tests(behavior_nodes: list[BehaviorNode], variables: Variables) -> (
        list)[BehaviorTest]:
    return [get_behavior_test(behavior_node, variables) for behavior_node in behavior_nodes]


def get_behavior_test(behavior_node: BehaviorNode, variables: Variables) -> BehaviorTest:
    test_collections = build_test_collections(variables, behavior_node)
    return BehaviorTest(test_collections, behavior_node)
