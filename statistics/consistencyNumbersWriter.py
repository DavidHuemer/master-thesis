from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def print_consistency_numbers(test_results: list[VerificationResult]):
    nr_consistent = len([result for result in test_results if result.consistent])
    nr_inconsistencies = len([result for result in test_results if not result.consistent])
    nr_unknown_inconsistencies = len([result for result in test_results if result.consistent is None])

    table = PrettyTable()
    table.field_names = ['Consistency type', 'Number of results']
    table.add_row(["Consistent", nr_consistent])
    table.add_row(["Not consistent", nr_inconsistencies])
    table.add_row(["Unknown inconsistency (exceptions)", nr_unknown_inconsistencies])

    log_info("Consistency types:")
    log_info(table.get_string())
