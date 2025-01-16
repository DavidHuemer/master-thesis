from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.testCollections import TestCollections
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info
from verification.result.verificationResultFactory import VerificationResultFactory
from testGeneration.testCaseGeneration.testCaseRunner import TestCaseRunner


class TestCollectionsRunner:
    def __init__(self, test_case_runner=TestCaseRunner()):
        self.test_case_runner = test_case_runner

    def run(self, test_class: JavaRuntimeClass, test_collections: TestCollections,
            consistency_test_case: ConsistencyTestCase, behavior: BehaviorNode) -> VerificationResult:
        log_info("Running test collections")

        # Steps to run test collections
        # 1. Run positive tests
        for test_case in test_collections.test_collection.test_cases:
            result = self.test_case_runner.run(test_class, test_case, consistency_test_case=consistency_test_case,
                                               behavior=behavior,
                                               csp_parameters=test_collections.test_collection.csp_parameters)

            if not result:
                return VerificationResultFactory.inconsistent_result(consistency_test_case,
                                                                     parameters=str(test_case.parameters))

        # 2. Run exception tests
        for signal_collection in test_collections.signal_collections:
            log_info(f"Running signal collection for {signal_collection.exception_type}")
            for test_case in signal_collection.test_cases:
                result = self.test_case_runner.run(test_class, test_case,
                                                   consistency_test_case=consistency_test_case,
                                                   behavior=behavior,
                                                   expected_exception=signal_collection.exception_type,
                                                   csp_parameters=signal_collection.csp_parameters)

                if not result:
                    return VerificationResultFactory.inconsistent_result(consistency_test_case)

        return VerificationResultFactory.consistent_result(consistency_test_case)
