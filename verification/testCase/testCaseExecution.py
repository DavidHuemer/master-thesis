import jpype

from codeExecution.runtime.codeExecution import CodeExecution
from definitions.codeExecution.result.executionResult import ExecutionResult
from helper.logs.loggingHelper import LoggingHelper


class TestCaseExecution:
    def __init__(self, code_execution=CodeExecution()):
        self.code_execution = code_execution

    def execute_method(self, test_instance, test_case, consistency_test_case) -> ExecutionResult:
        result = self.get_original_result(test_instance, test_case, consistency_test_case)
        if isinstance(result, ExecutionResult):
            return result

        if isinstance(result, jpype.JArray):
            result = list(result)

        return ExecutionResult(result=result, parameters=test_case.parameters)

    def get_original_result(self, test_instance, test_case, consistency_test_case):
        try:
            return self.code_execution.execute(test_instance, test_case=test_case,
                                               consistency_test_case=consistency_test_case)
        except Exception as e:
            LoggingHelper().log_info(f"Error while executing java method: {e}")
            name = e.getClass().getName()
            return ExecutionResult(result=None, parameters=test_case.parameters, exception=name)
