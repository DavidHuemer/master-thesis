from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper


class ConsistencyNumbersWriter:

    @staticmethod
    def print_consistency_numbers(test_results: list[VerificationResult]):
        nr_consistent = len(list(filter(lambda x: x.consistent is True, test_results)))
        nr_inconsistencies = len(list(filter(lambda x: x.consistent is False, test_results)))
        nr_unknown_inconsistencies = len(list(filter(lambda x: x.consistent is None, test_results)))

        table = PrettyTable()
        table.field_names = ['Consistency type', 'Number of results']
        table.add_row(['Consistent', nr_consistent])
        table.add_row(['Not consistent', nr_inconsistencies])
        table.add_row(['Unknown inconsistency (exceptions)', nr_unknown_inconsistencies])

        table_str = table.get_string()
        LoggingHelper.log_info("Consistency types:", show_level=False)
        LoggingHelper.log_info(table_str, show_level=False)
