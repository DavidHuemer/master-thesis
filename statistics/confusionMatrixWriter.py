from typing import List, Optional

from dependency_injector.providers import Callable
from prettytable import PrettyTable
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import log_info


def write_confusion_matrix(verification_results: List[VerificationResult]):
    results_with_expected_result = [result for result in verification_results
                                    if result.consistency_test_case.expected_result is not None]

    expected_consistencies = [result for result in results_with_expected_result
                              if result.get_expected_result() is True]

    expected_inconsistencies = [result for result in results_with_expected_result
                                if result.get_expected_result() is False]

    confusion_data = {
        "true_positive": count_results(expected_consistencies, True),
        "false_negative": count_results(expected_consistencies, False),
        "false_positive": count_results(expected_inconsistencies, True),
        "true_negative": count_results(expected_inconsistencies, False),
        "expected_consistent_got_unknown": count_results(expected_consistencies, None),
        "expected_inconsistent_got_unknown": count_results(expected_inconsistencies, None),
    }

    table = PrettyTable()
    table.field_names = [
        "",
        f"Expected consistent ({len(expected_consistencies)})",
        f"Expected not consistent ({len(expected_inconsistencies)})"
    ]

    table.add_row([
        "Got consistent",
        confusion_data["true_positive"],
        confusion_data["false_positive"]
    ])
    table.add_row([
        "Got not consistent",
        confusion_data["false_negative"],
        confusion_data["true_negative"]
    ])
    table.add_row([
        "Got unknown",
        confusion_data["expected_consistent_got_unknown"],
        confusion_data["expected_inconsistent_got_unknown"]
    ])

    log_info("Confusion matrix:")
    log_info(table.get_string())


def filter_results_by_condition(results: List[VerificationResult], condition) \
        -> List[VerificationResult]:
    """Filter a list of results based on a given condition."""
    return list(filter(condition, results))


def count_results(results: List[VerificationResult], expected_result: Optional[bool]) -> int:
    """Count results where the actual result matches the expected result."""
    return len([result for result in results if result.consistent is expected_result])
