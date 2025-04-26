import os

from codeExecution.duplication.javaVariableExtractor import initialize_instance_variables, \
    update_instance_variables
from codeExecution.runtime.javaClassInstantiation import instantiate_clazz
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.envKeys import VALIDATION_TIMEOUT
from definitions.parameters.Variables import Variables
from helper.timeout.timeoutHelper import TimeoutHelper
from testGeneration.testCaseGeneration.testCaseExecution import execute_method
from verification.resultVerification.executionVerifier import ExecutionVerifier


class TestCaseRunner:
    def __init__(self, timeout_helper=None):
        self.timeout_helper = timeout_helper or TimeoutHelper()
        self.execution_verifier = ExecutionVerifier()
        self.timeout = float(os.getenv(VALIDATION_TIMEOUT))

    # TODO: Return more than just a boolean (e.g. why the test failed)
    def run(self, test_class: JavaRuntimeClass,
            variables: Variables, consistency_test_case: ConsistencyTestCase,
            behavior: BehaviorNode, expected_exception=None) -> bool:
        # Steps to run a test case:
        # 1. Get instance of the testing class (Constructor has already been checked
        test_instance = instantiate_clazz(test_class)
        initialize_instance_variables(variables.instance_parameters, test_instance, test_class)

        # 2. Get the current parameters list of the class instance before the execution

        # 3. execute the method with the parameters
        execution_result = execute_method(test_instance, variables, consistency_test_case)
        update_instance_variables(variables.instance_parameters, test_instance, test_class)

        return self.timeout_helper.run_with_timeout(
            method=lambda stop_event: self.execution_verifier.verify(execution_result=execution_result,
                                                                     behavior=behavior,
                                                                     expected_exception=expected_exception,
                                                                     consistency_test_case=consistency_test_case,
                                                                     variables=variables,
                                                                     stop_event=stop_event), timeout=self.timeout)
