import time

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info, log_error
from statistics.category_writer import write_category_results

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
    write_category_results(test_results)
    # write_no_expected_results_statistics(test_results)
    print_spacing()
    write_test_cases_table(test_results)
    print_spacing()
    write_success(test_results)

    print_logs(test_results)


def print_logs(test_results: list[VerificationResult]):
    log_info("printing logs...")

    current_timestamp = current_timestamp = int(time.time() * 1000)

    # Open file data/logs_<timestamp>.txt
    file_name = f"data/logs_{current_timestamp}.txt"
    with open(file_name, "w") as f:
        for result in test_results:
            if result.logs:
                f.write(f"Consistency Test: {result.consistency_test_case.method_info.name}\n")
                f.write("Logs:\n")
                for log in result.logs:
                    f.write(f"{log}\n")
                f.write("\n")

    log_info("logs printing finished")


def print_spacing():
    log_info("\n\n\n")
