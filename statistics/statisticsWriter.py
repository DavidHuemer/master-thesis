from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info, log_error

from statistics.confusionMatrixWriter import write_confusion_matrix
from statistics.consistencyNumbersWriter import print_consistency_numbers
from statistics.noExpectedResultsWriter import write_no_expected_results_statistics
from statistics.successWriter import write_success
from statistics.testCasesTableWriter import write_test_cases_table


def write_statistics(test_results: list[VerificationResult]):
    log_info('Statistics:')

    print_consistency_numbers(test_results)
    print_spacing()
    write_confusion_matrix(test_results)
    print_spacing()
    write_no_expected_results_statistics(test_results)
    print_spacing()
    write_test_cases_table(test_results)
    print_spacing()
    write_success(test_results)


def print_spacing():
    log_info("\n\n\n")
