from prettytable import PrettyTable

from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def write_category_results(test_results: list[VerificationResult]):
    table = PrettyTable()
    table.field_names = [
        "Category",
        "Results",
    ]

    categories = ["sequential", "branched", "loop", "nested-loop"]
    for category in categories:

        category_test_results = [
            result for result in test_results if result.consistency_test_case.expected_result.category == category
        ]

        total_count = len(category_test_results)

        correct_count = len([
            result for result in category_test_results if result.consistent == result.get_expected_result()
        ])

        table.add_row([
            f"{category} ({total_count})",
            correct_count if total_count > 0 else "-"
        ])

    log_info("Category results:")
    log_info(table.get_string())
