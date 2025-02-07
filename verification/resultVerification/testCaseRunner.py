from dependency_injector.wiring import inject

from codeExecution.duplication.javaDuplicationHelper import duplicate_java_class
from codeExecution.duplication.javaVariableExtractor import get_parameters
from codeExecution.runtime.javaClassInstantiation import instantiate_clazz
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.resultInstances import ResultInstances
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.verification.testCase import TestCase
from helper.timeout.timeoutHelper import TimeoutHelper
from testGeneration.testCaseGeneration.testCaseExecution import execute_method
from verification.resultVerification.executionVerifier import ExecutionVerifier
import jpype.imports




class TestCaseRunner:
    def __init__(self, timeout_helper=TimeoutHelper()):
        self.timeout_helper = timeout_helper

    # TODO: Return more than just a boolean (e.g. why the test failed)
    def run(self, test_class: JavaRuntimeClass,
            test_case: TestCase, consistency_test_case: ConsistencyTestCase, csp_parameters: CSPParameters,
            behavior: BehaviorNode, expected_exception=None) -> bool:
        # Steps to run a test case:
        # 1. Get instance of the testing class (Constructor has already been checked
        test_instance = instantiate_clazz(test_class)

        # 2. Get the current parameters list of the class instance before the execution
        old_variables = get_parameters(test_instance, test_class)

        old_duplicate = duplicate_java_class(test_class, test_instance)

        # 3. execute the method with the parameters
        execution_result = execute_method(test_instance, test_case, consistency_test_case)
        new_variables = get_parameters(test_instance, test_class)

        result_parameters = ResultParameters(method_call_parameters=execution_result.parameters,
                                             old_instance_variables=old_variables,
                                             new_instance_variables=new_variables,
                                             csp_parameters=csp_parameters)

        result_instances = ResultInstances(old=old_duplicate, new=test_instance)

        return self.timeout_helper.run_with_timeout(
            method=lambda stop_event: ExecutionVerifier().verify(execution_result=execution_result,
                                                                 result_parameters=result_parameters,
                                                                 behavior=behavior,
                                                                 expected_exception=expected_exception,
                                                                 consistency_test_case=consistency_test_case,
                                                                 test_case=test_case,
                                                                 result_instances=result_instances,
                                                                 stop_event=stop_event), timeout=500)
