from codetiming import Timer

from codeExecution.runtime.javaClassConstructorHelper import JavaClassConstructorHelper
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info
from testGeneration.testCollections.testCollectionsRunner import run_test_collections
from verification.result.verificationResultFactory import VerificationResultFactory

behavior_runner_timer = Timer(name="run_behaviors", logger=None)


@behavior_runner_timer
def run_behaviors(test_class: JavaRuntimeClass, behaviors: list[BehaviorTest],
                  consistency_test_case: ConsistencyTestCase) -> VerificationResult:
    log_info("Running test behaviors")

    # Check that test_class has empty constructor
    if not JavaClassConstructorHelper().has_empty_constructors(test_class):
        raise Exception("Class has no empty constructor")

    for behavior in behaviors:
        behavior_result = run_behavior(behavior=behavior,
                                       test_class=test_class,
                                       consistency_test_case=consistency_test_case)
        if not behavior_result.consistent:
            return VerificationResultFactory.inconsistent_result(consistency_test_case)

    return VerificationResultFactory.consistent_result(consistency_test_case)


def run_behavior(behavior: BehaviorTest, test_class: JavaRuntimeClass,
                 consistency_test_case: ConsistencyTestCase) -> VerificationResult:
    log_info(f"Running behavior: {str(behavior)}")

    return run_test_collections(test_class=test_class,
                                test_collections=behavior.test_collections,
                                consistency_test_case=consistency_test_case,
                                behavior=behavior.behavior_node)
