import jpype

from definitions.codeExecution.result.executionException import ExecutionException


def is_exception_type_allowed(exception: ExecutionException, allowed_exceptions: list[str]):
    """
    Check if the exception is a subclass of the allowed exceptions
    :param exception: The actual exception
    :param allowed_exceptions: The allowed exceptions
    :return: True if the exception is a subclass of the allowed exceptions, False otherwise
    """
    return (not len(allowed_exceptions) > 0 or
            any([verify_exception_subclass(exception, allowed_exception) for allowed_exception in allowed_exceptions]))


def verify_exception_subclass(exception: ExecutionException, expected_exception: str):
    """
    Check if the exception is a subclass of the expected exception
    :param exception: The actual exception
    :param expected_exception: The expected exception
    :return: True if the exception is a subclass of the expected exception, False otherwise
    """
    expected_exception_instance = jpype.JClass(f'java.lang.{expected_exception}')
    thrown_exception_instance = jpype.JClass(exception.full_name)

    return issubclass(thrown_exception_instance, expected_exception_instance)
