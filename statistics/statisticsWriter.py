from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from prettytable import PrettyTable


class StatisticsWriter:
    """
    Write statistics about the inconsistency tests
    """

    def __init__(self):
        pass

    def write(self, test_results: list[VerificationResult]):
        LoggingHelper.log_info('Statistics:', show_level=False)

        # Print number of tests with no inconsistencies and number of tests with inconsistencies
        self.print_inconsistency_numbers(test_results)
        self.print_spacing()
        self.print_confusion_matrix(test_results)
        self.print_spacing()
        self.print_results(test_results)

        # Print confusion matrix
        pass

    def print_inconsistency_numbers(self, test_results: list[VerificationResult]):
        # Nr of test_results with inconsistency False
        nr_inconsistencies = len(list(filter(lambda x: x.inconsistency is True, test_results)))
        nr_no_inconsistencies = len(list(filter(lambda x: x.inconsistency is False, test_results)))
        nr_unknown_inconsistencies = len(list(filter(lambda x: x.inconsistency is None, test_results)))

        table = PrettyTable()
        table.field_names = ['Inconsistency type', 'Number of results']
        table.add_row(['Inconsistency', nr_inconsistencies])
        table.add_row(['No inconsistency', nr_no_inconsistencies])
        table.add_row(['Unknown inconsistency (exceptions)', nr_unknown_inconsistencies])

        table_str = table.get_string()
        LoggingHelper.log_info("Inconsistency types:", show_level=False)
        LoggingHelper.log_info(table_str, show_level=False)

    def print_spacing(self):
        LoggingHelper.log_info("\n\n\n", show_level=False)

    def print_confusion_matrix(self, test_results: list[VerificationResult]):
        results_with_expected_results: list[VerificationResult] = list(
            filter(lambda x: x.inconsistency_test_case.expected_result is not None, test_results))

        # Expected number of inconsistencies
        expected_inconsistencies = len(list(
            filter(lambda x:
                   x.inconsistency_test_case.expected_result.expected_result is False, results_with_expected_results)))

        # Expected number of no inconsistencies
        expected_no_inconsistencies = len(list(
            filter(lambda x:
                   x.inconsistency_test_case.expected_result.expected_result is True, results_with_expected_results)))

        # True positives
        true_positives = len(list(
            filter(lambda x:
                   x.inconsistency is True
                   and x.inconsistency_test_case.expected_result.expected_result is False,
                   results_with_expected_results)))

        # False positives
        false_positives = len(list(
            filter(lambda x:
                   x.inconsistency is True
                   and x.inconsistency_test_case.expected_result.expected_result is True,
                   results_with_expected_results)))

        # False negatives
        false_negatives = len(list(
            filter(lambda x:
                   x.inconsistency is False
                   and x.inconsistency_test_case.expected_result.expected_result is False,
                   results_with_expected_results)))

        # True negatives
        true_negatives = len(list(
            filter(lambda x:
                   x.inconsistency is False
                   and x.inconsistency_test_case.expected_result.expected_result is True,
                   results_with_expected_results)))

        # Expected true but got unknown
        expected_true_got_unknown = len(list(
            filter(lambda x:
                   x.inconsistency is None
                   and x.inconsistency_test_case.expected_result.expected_result is True,
                   results_with_expected_results)))

        # Expected false but got unknown
        expected_false_got_unknown = len(list(
            filter(lambda x:
                   x.inconsistency is None
                   and x.inconsistency_test_case.expected_result.expected_result is False,
                   results_with_expected_results)))

        table = PrettyTable()
        table.field_names = ['',
                             f'Expected inconsistency ({expected_inconsistencies})',
                             f'Expected no inconsistency ({expected_no_inconsistencies})']

        table.add_row(['Got inconsistency',
                       f'{true_positives}/{expected_inconsistencies}',
                       f'{false_positives}/0'])

        table.add_row(['Got no inconsistency',
                       f'{false_negatives}/0',
                       f'{true_negatives}/{expected_no_inconsistencies}'])

        table.add_row(['Got unknown (exception)',
                       f'{expected_true_got_unknown}/0',
                       f'{expected_false_got_unknown}/0'])

        table_str = table.get_string()
        LoggingHelper.log_info("Confusion matrix:", show_level=False)
        LoggingHelper.log_info(table_str, show_level=False)

    def print_results(self, test_results: list[VerificationResult]):
        for test_result in test_results:
            LoggingHelper.log_info(f"Test case:", show_level=False)
            LoggingHelper.log_info(test_result.inconsistency_test_case.get_name(), show_level=False)

            LoggingHelper.log_info(f"Expected result: "
                                   f"{test_result.inconsistency_test_case.get_expected_result_str()}",
                                   show_level=False)

            LoggingHelper.log_info(f"Result: ", show_level=False)

            if test_result.exception is not None:
                LoggingHelper.log_error(test_result.exception, show_level=False)
                LoggingHelper.log_error(test_result.message, show_level=False)
            else:
                if test_result.inconsistency is True:
                    LoggingHelper.log_info("Inconsistency found", show_level=False)
                elif test_result.inconsistency is False:
                    LoggingHelper.log_info("No inconsistency found", show_level=False)
                else:
                    LoggingHelper.log_info("Unknown inconsistency (exception)", show_level=False)
