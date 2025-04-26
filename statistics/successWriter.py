from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def write_success(test_results: list[VerificationResult]):
    results = [result for result in test_results if result.consistency_test_case.expected_result is not None]

    successful_results = [result for result in results if result.consistent == result.get_expected_result()]

    success = len(successful_results) * 100 / len(results)
    log_info(f"Success rate: {success}%")


def get_results_with_expected_result(results: list[VerificationResult]):
    return list(filter(lambda x: x.consistency_test_case.expected_result is not None, results))
