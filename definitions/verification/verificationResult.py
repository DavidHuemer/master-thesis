from definitions.inconsistencyTestCase import InconsistencyTestCase


class VerificationResult:
    def __init__(self, inconsistency_test_case: InconsistencyTestCase, inconsistency: bool | None, message: str | None,
                 exception: Exception | None):
        self.inconsistency_test_case = inconsistency_test_case
        self.inconsistency = inconsistency
        self.message = message
        self.exception = exception

    def get_error_message(self):
        if self.exception is None:
            return None

        if hasattr(self.exception, 'message'):
            return self.exception.message

        if hasattr(self.exception, 'args') and len(self.exception.args) > 0:
            return self.exception.args[0]

        return self.exception.message if hasattr(self.exception, 'message') else 'Exception occurred'

    def get_message(self):
        return self.message if self.message is not None else 'No further message'

    def __str__(self):
        return f'Inconsistency: {self.inconsistency}, Message: {self.get_message()}, Error: {self.get_error_message()}'
