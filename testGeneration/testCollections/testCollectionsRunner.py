from concurrent import futures

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.testCollections import TestCollections
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info
from verification.result.verificationResultFactory import VerificationResultFactory
from verification.resultVerification.testCaseRunner import TestCaseRunner


def run_test_collections(test_class: JavaRuntimeClass, test_collections: TestCollections,
                         consistency_test_case: ConsistencyTestCase, behavior: BehaviorNode) -> VerificationResult:
    log_info("Running test collections")

    # Steps to run test collections
    # 1. Run positive tests

    # return VerificationResultFactory.consistent_result(consistency_test_case)
    runner = TestCaseRunner()

    for variables in test_collections.test_collection.test_cases:
        result = runner.run(test_class, variables, consistency_test_case=consistency_test_case,
                            behavior=behavior)

        if not result:
            return VerificationResultFactory.inconsistent_result(consistency_test_case,
                                                                 parameters=variables.get_method_call_visualization())

    # 2. Run exception tests
    for signal_collection in test_collections.signal_collections:
        log_info(f"Running signal collection for {signal_collection.exception_type}")
        for variables in signal_collection.test_cases:
            result = runner.run(test_class, variables,
                                consistency_test_case=consistency_test_case,
                                behavior=behavior,
                                expected_exception=signal_collection.exception_type)

            if not result:
                return VerificationResultFactory.inconsistent_result(consistency_test_case)

    return VerificationResultFactory.consistent_result(consistency_test_case)
