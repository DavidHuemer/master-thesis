from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper

from statistics.confusionMatrixWriter import ConfusionMatrixWriter
from statistics.consistencyNumbersWriter import ConsistencyNumbersWriter
from statistics.testCasesTableWriter import TestCasesTableWriter


class StatisticsWriter:
    """
    Write statistics about the inconsistency tests
    """

    def __init__(self, consistency_numbers_writer=ConsistencyNumbersWriter(),
                 confusion_matrix_writer=ConfusionMatrixWriter(),
                 test_cases_table_writer=TestCasesTableWriter()):
        self.consistency_numbers_writer = consistency_numbers_writer
        self.confusion_matrix_writer = confusion_matrix_writer
        self.test_cases_table_writer = test_cases_table_writer

    def write(self, test_results: list[VerificationResult]):
        LoggingHelper.log_info('Statistics:', show_level=False)

        # Print number of tests with no inconsistencies and number of tests with inconsistencies

        # self.confusion_matrix_writer.write_confusion_matrix(test_results)
        self.consistency_numbers_writer.print_consistency_numbers(test_results)
        self.print_spacing()
        self.confusion_matrix_writer.write_confusion_matrix(test_results)
        self.print_spacing()
        self.test_cases_table_writer.write_test_cases_table(test_results)
        self.print_spacing()
        self.print_results(test_results)

        # Print confusion matrix
        pass

    def print_spacing(self):
        LoggingHelper.log_info("\n\n\n", show_level=False)

    def print_results(self, test_results: list[VerificationResult]):
        for test_result in test_results:
            LoggingHelper.log_info(f"Test case:", show_level=False)
            LoggingHelper.log_info(test_result.consistency_test_case.get_name(), show_level=False)

            LoggingHelper.log_info(f"Expected result: "
                                   f"{test_result.consistency_test_case.get_expected_result_str()}",
                                   show_level=False)

            LoggingHelper.log_info(f"Result: ", show_level=False)

            if test_result.exception is not None:
                LoggingHelper.log_error(test_result.exception, show_level=False)
                LoggingHelper.log_error(test_result.message, show_level=False)
            else:
                if test_result.consistent is True:
                    LoggingHelper.log_info("Inconsistency found", show_level=False)
                elif test_result.consistent is False:
                    LoggingHelper.log_info("No inconsistency found", show_level=False)
                else:
                    LoggingHelper.log_info("Unknown inconsistency (exception)", show_level=False)
