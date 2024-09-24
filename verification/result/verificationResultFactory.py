from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.verificationResult import VerificationResult


class VerificationResultFactory:
    @staticmethod
    def by_exception(inconsistency_test_case: ConsistencyTestCase, exception: Exception):
        message = None

        if hasattr(exception, 'message'):
            message = exception.message

        elif hasattr(exception, 'args') and len(exception.args) > 0:
            message = exception.args[0]

        return VerificationResult(inconsistency_test_case,
                                  consistent=None,
                                  parameters=None,
                                  message=message,
                                  exception=exception)

    @staticmethod
    def inconsistent_result(inconsistency_test_case, parameters: str | None = None):
        return VerificationResult(inconsistency_test_case,
                                  consistent=False,
                                  parameters=parameters,
                                  message=None,
                                  exception=None)

    @staticmethod
    def consistent_result(inconsistency_test_case):
        return VerificationResult(inconsistency_test_case,
                                  consistent=True,
                                  parameters=None,
                                  message=None,
                                  exception=None)
