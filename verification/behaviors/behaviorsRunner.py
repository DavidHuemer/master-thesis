from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from verification.result.verificationResultFactory import VerificationResultFactory
from verification.testCollections.testCollectionsRunner import TestCollectionsRunner


class BehaviorsRunner:
    def __init__(self, test_collections_runner=TestCollectionsRunner()):
        self.test_collections_runner = test_collections_runner

    def run(self, test_class: JavaRuntimeClass, behaviors: list[BehaviorTest],
            consistency_test_case: ConsistencyTestCase) -> VerificationResult:
        LoggingHelper.log_info("Running test behaviors")

        for behavior in behaviors:
            LoggingHelper.log_info(f"Running behavior: {behavior}")
            behavior_result = self.run_behavior(behavior, test_class, consistency_test_case)
            if not behavior_result.consistent:
                return VerificationResultFactory.inconsistent_result(consistency_test_case)

        return VerificationResultFactory.consistent_result(consistency_test_case)

    def run_behavior(self, behavior: BehaviorTest, test_class: JavaRuntimeClass,
                     consistency_test_case: ConsistencyTestCase) -> VerificationResult:
        return self.test_collections_runner.run(test_class=test_class,
                                                test_collections=behavior.test_collections,
                                                consistency_test_case=consistency_test_case,
                                                behavior=behavior.behavior_node)
