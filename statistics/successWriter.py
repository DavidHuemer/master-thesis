from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


class SuccessWriter:
    def write_success(self, test_results: list[VerificationResult]):
        results = self.get_results_with_expected_result(test_results)

        successful_results = list(
            filter(lambda x: x.consistent == x.consistency_test_case.expected_result.expected_result, results))
        successful_len = len(successful_results)

        success = successful_len * 100 / len(results)
        log_info(f"Success rate: {success}%")

    @staticmethod
    def get_results_with_expected_result(results: list[VerificationResult]):
        return list(filter(lambda x: x.consistency_test_case.expected_result is not None, results))
