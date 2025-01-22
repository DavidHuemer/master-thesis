from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def print_consistency_numbers(test_results: list[VerificationResult]):
    nr_consistent = sum(1 for x in test_results if x.consistent is True)
    nr_inconsistencies = sum(1 for x in test_results if x.consistent is False)
    nr_unknown_inconsistencies = sum(1 for x in test_results if x.consistent is None)

    table = PrettyTable()
    table.field_names = ['Consistency type', 'Number of results']
    consistency_data = [
        ('Consistent', nr_consistent),
        ('Not consistent', nr_inconsistencies),
        ('Unknown inconsistency (exceptions)', nr_unknown_inconsistencies)
    ]

    for row in consistency_data:
        table.add_row(row)

    table_str = table.get_string()
    log_info("Consistency types:")
    log_info(table_str)
