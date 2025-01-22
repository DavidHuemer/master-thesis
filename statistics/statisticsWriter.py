from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info, log_error

from statistics.confusionMatrixWriter import write_confusion_matrix
from statistics.consistencyNumbersWriter import print_consistency_numbers
from statistics.noExpectedResultsWriter import write_no_expected_results_statistics
from statistics.successWriter import SuccessWriter
from statistics.testCasesTableWriter import write_test_cases_table


def write_statistics(test_results: list[VerificationResult]):
    log_info('Statistics:')

    # Print number of tests with no inconsistencies and number of tests with inconsistencies

    # self.confusion_matrix_writer.write_confusion_matrix(test_results)
    print_consistency_numbers(test_results)
    # self.print_spacing()
    write_confusion_matrix(test_results)
    # self.print_spacing()
    write_no_expected_results_statistics(test_results)
    # self.print_spacing()
    write_test_cases_table(test_results)
    # self.print_spacing()
    # self.success_writer.write_success(test_results)

# class StatisticsWriter:
#     """
#     Write statistics about the consistency tests
#     """
#
#     def __init__(self, consistency_numbers_writer=ConsistencyNumbersWriter(),
#                  confusion_matrix_writer=ConfusionMatrixWriter(),
#                  test_cases_table_writer=TestCasesTableWriter(),
#                  success_writer=SuccessWriter()):
#         self.consistency_numbers_writer = consistency_numbers_writer
#         self.confusion_matrix_writer = confusion_matrix_writer
#         self.test_cases_table_writer = test_cases_table_writer
#         self.success_writer = success_writer
#
#     def write(self, test_results: list[VerificationResult]):
#         log_info('Statistics:')
#
#         # Print number of tests with no inconsistencies and number of tests with inconsistencies
#
#         # self.confusion_matrix_writer.write_confusion_matrix(test_results)
#         self.consistency_numbers_writer.print_consistency_numbers(test_results)
#         self.print_spacing()
#         self.confusion_matrix_writer.write_confusion_matrix(test_results)
#         self.print_spacing()
#         self.test_cases_table_writer.write_test_cases_table(test_results)
#         self.print_spacing()
#         self.success_writer.write_success(test_results)
#
#         # Print confusion matrix
#         pass
#
#     @staticmethod
#     def print_spacing():
#         log_info("\n\n\n")
#
#     @staticmethod
#     def print_results(test_results: list[VerificationResult]):
#         for test_result in test_results:
#             log_info(f"Test case:")
#             log_info(test_result.consistency_test_case.get_name())
#
#             log_info(f"Expected result: "
#                      f"{test_result.consistency_test_case.get_expected_result_str()}")
#
#             log_info(f"Result: ")
#
#             if test_result.exception is not None:
#                 log_error(test_result.exception)
#                 log_error(test_result.message)
#             else:
#                 if test_result.consistent is True:
#                     log_info("Inconsistency found")
#                 elif test_result.consistent is False:
#                     log_info("No inconsistency found")
#                 else:
#                     log_info("Unknown inconsistency (exception)")
