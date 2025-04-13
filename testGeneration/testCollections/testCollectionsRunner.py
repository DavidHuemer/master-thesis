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

    # with futures.ThreadPoolExecutor() as executor:
    #     result = executor.map(TestCaseRunner().run, [test_class] * len(test_collections.test_collection.test_cases),
    #                           test_collections.test_collection.test_cases,
    #                           [consistency_test_case] * len(test_collections.test_collection.test_cases),
    #                           [test_collections.test_collection.csp_parameters] * len(test_collections.test_collection.test_cases),
    #                           [behavior] * len(test_collections.test_collection.test_cases))

        #print(list(result))

        # f = executor.submit(TestCaseRunner().run, test_class, test_collections.test_collection.test_cases[0],
        #                     consistency_test_case=consistency_test_case,
        #                     behavior=behavior, csp_parameters=test_collections.test_collection.csp_parameters)

        #<result = f.result()

        # results = executor.map(
        #     lambda test_case: TestCaseRunner().run(test_class, test_case, consistency_test_case=consistency_test_case,
        #                                  behavior=behavior,
        #                                  csp_parameters=test_collections.test_collection.csp_parameters),
        #     test_collections.test_collection.test_cases)
        # for result in results:
        #     if not result:
        #         return VerificationResultFactory.consistent_result(consistency_test_case)
        # return VerificationResultFactory.inconsistent_result(consistency_test_case,
        #                                                      parameters=str(test_case.parameters))

    for test_case in test_collections.test_collection.test_cases:
        result = runner.run(test_class, test_case, consistency_test_case=consistency_test_case,
                            behavior=behavior,
                            csp_parameters=test_collections.test_collection.csp_parameters)

        if not result:
            return VerificationResultFactory.inconsistent_result(consistency_test_case,
                                                                 parameters=str(test_case.parameters))

    # 2. Run exception tests
    # for signal_collection in test_collections.signal_collections:
    #     log_info(f"Running signal collection for {signal_collection.exception_type}")
    #     for test_case in signal_collection.test_cases:
    #         result = TestCaseRunner().run(test_class, test_case,
    #                                       consistency_test_case=consistency_test_case,
    #                                       behavior=behavior,
    #                                       expected_exception=signal_collection.exception_type,
    #                                       csp_parameters=signal_collection.csp_parameters)
    #
    #         if not result:
    #             return VerificationResultFactory.inconsistent_result(consistency_test_case)

    return VerificationResultFactory.consistent_result(consistency_test_case)
