from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.verification.verificationResult import VerificationResult
from pipeline.consistencyPipelineLogsContainer import consistency_logs, get_consistency_logs


class VerificationResultFactory:
    @staticmethod
    def by_exception(consistency_test_case: ConsistencyTestCase, exception: Exception):
        message = None

        if hasattr(exception, 'message'):
            message = exception.message

        elif hasattr(exception, 'args') and len(exception.args) > 0:
            message = exception.args[0]

        return VerificationResult(consistency_test_case,
                                  consistent=None,
                                  parameters=None,
                                  message=message,
                                  exception=exception,
                                  logs=get_consistency_logs())

    @staticmethod
    def inconsistent_result(consistency_test_case, parameters: str | None = None):
        return VerificationResult(consistency_test_case,
                                  consistent=False,
                                  parameters=parameters,
                                  message=None,
                                  exception=None,
                                  logs=get_consistency_logs())

    @staticmethod
    def consistent_result(consistency_test_case):
        return VerificationResult(consistency_test_case,
                                  consistent=True,
                                  parameters=None,
                                  message=None,
                                  exception=None,
                                  logs=get_consistency_logs())
