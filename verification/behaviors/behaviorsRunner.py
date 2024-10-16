import time

from codeExecution.runtime.javaClassConstructorHelper import JavaClassConstructorHelper
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.behaviorTest import BehaviorTest
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from verification.result.verificationResultFactory import VerificationResultFactory
from verification.testCollections.testCollectionsRunner import TestCollectionsRunner


class BehaviorsRunner:
    def __init__(self, test_collections_runner=TestCollectionsRunner(),
                 constructor_helper=JavaClassConstructorHelper()):
        self.test_collections_runner = test_collections_runner
        self.constructor_helper = constructor_helper

    def run(self, test_class: JavaRuntimeClass, behaviors: list[BehaviorTest],
            consistency_test_case: ConsistencyTestCase) -> VerificationResult:
        LoggingHelper.log_info("Running test behaviors")

        # Check that test_class has empty constructor
        if not self.constructor_helper.has_empty_constructors(test_class):
            raise Exception("Class has no empty constructor")

        for behavior in behaviors:
            behavior_result = self.run_behavior(behavior, test_class, consistency_test_case)
            if not behavior_result.consistent:
                return VerificationResultFactory.inconsistent_result(consistency_test_case)

        return VerificationResultFactory.consistent_result(consistency_test_case)

    def run_behavior(self, behavior: BehaviorTest, test_class: JavaRuntimeClass,
                     consistency_test_case: ConsistencyTestCase) -> VerificationResult:
        LoggingHelper.log_info(f"Running behavior: {str(behavior)}")
        return self.test_collections_runner.run(test_class=test_class,
                                                test_collections=behavior.test_collections,
                                                consistency_test_case=consistency_test_case,
                                                behavior=behavior.behavior_node)
