from definitions.consistencyTestCase import ConsistencyTestCase


class VerificationResult:
    def __init__(self, consistency_test_case: ConsistencyTestCase, consistent: bool | None, parameters: str | None,
                 message: str | None,
                 exception: Exception | None):
        self.consistency_test_case = consistency_test_case
        self.consistent = consistent
        self.parameters = parameters
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
        return f'Consistency: {self.consistent}, Message: {self.get_message()}, Error: {self.get_error_message()}'
