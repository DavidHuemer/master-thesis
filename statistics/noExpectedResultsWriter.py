from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def write_no_expected_results_statistics(test_results: list[VerificationResult]):
    test_results_with_no_expected_results = [
        x for x in test_results if x.consistency_test_case.expected_result is None
    ]

    nr_no_expected_results = len(test_results_with_no_expected_results)
    log_info(f"Nr of tests with no expected results: {nr_no_expected_results}")

    for test_result in test_results_with_no_expected_results:
        log_info(
            f"Test with no expected result: {test_result.consistency_test_case.java_code.class_name}: "
            f"{test_result.consistency_test_case.method_info} - {test_result.consistent}")
