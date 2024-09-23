from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper


class ConfusionMatrixWriter:
    def __init__(self):
        pass

    def write_confusion_matrix(self, test_results: list[VerificationResult]):
        results = self.get_results_with_expected_result(test_results)
        expected_consistencies = self.filter_by_expected_result(True, results)
        expected_inconsistencies = self.filter_by_expected_result(False, results)

        true_consistent = self.get_confusion_data(True, True, results)
        false_not_consistent = self.get_confusion_data(False, True, results)

        false_consistent = self.get_confusion_data(False, True, results)
        true_not_consistent = self.get_confusion_data(False, False, results)

        expected_consistent_got_unknown = self.get_confusion_data(True, None, results)
        expected_inconsistent_got_unknown = self.get_confusion_data(False, None, results)

        table = PrettyTable()
        table.field_names = ['',
                             f'Expected consistent ({len(expected_consistencies)})',
                             f'Expected not consistent ({len(expected_inconsistencies)})']

        table.add_row(['Got consistent', true_consistent, false_consistent])
        table.add_row(['Got not consistent', false_not_consistent, true_not_consistent])

        table.add_row(['Got unknown', expected_consistent_got_unknown, expected_inconsistent_got_unknown])

        table_str = table.get_string()
        LoggingHelper.log_info("Confusion matrix:", show_level=False)
        LoggingHelper.log_info(table_str, show_level=False)

    @staticmethod
    def get_results_with_expected_result(results: list[VerificationResult]):
        return list(filter(lambda x: x.consistency_test_case.expected_result is not None, results))

    @staticmethod
    def filter_by_expected_result(predicate, results: list[VerificationResult]):
        return list(filter(lambda x: x.consistency_test_case.expected_result.expected_result is predicate, results))

    @staticmethod
    def get_confusion_data(expected_result, result, results):
        return len(list(
            filter(lambda x:
                   x.consistent is result
                   and x.consistency_test_case.expected_result.expected_result is expected_result,
                   results)))
