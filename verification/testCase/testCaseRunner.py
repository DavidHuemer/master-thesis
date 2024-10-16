from codeExecution.duplication.javaDuplicationHelper import JavaDuplicationHelper
from codeExecution.duplication.javaVariableExtractor import JavaVariableExtractor
from codeExecution.runtime.javaClassInstantiation import JavaClassInstantiation
from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.codeExecution.result.resultInstances import ResultInstances
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.csp.parameters.cspParameters import CSPParameters
from definitions.evaluations.csp.parameters.resultParameters import ResultParameters
from definitions.verification.testCase import TestCase
from verification.resultVerification.executionVerifier import ExecutionVerifier
from verification.testCase.testCaseExecution import TestCaseExecution


class TestCaseRunner:
    def __init__(self, java_class_instantiation=JavaClassInstantiation(),
                 java_duplication_helper=JavaDuplicationHelper(),
                 test_case_execution=TestCaseExecution(),
                 execution_verifier=ExecutionVerifier(),
                 java_variable_extractor=JavaVariableExtractor()):
        self.java_class_instantiation = java_class_instantiation
        self.java_duplication_helper = java_duplication_helper
        self.test_case_execution = test_case_execution
        self.execution_verifier = execution_verifier
        self.java_variable_extractor = java_variable_extractor

    # TODO: Return more than just a boolean (e.g. why the test failed)
    def run(self, test_class: JavaRuntimeClass,
            test_case: TestCase, consistency_test_case: ConsistencyTestCase, csp_parameters: CSPParameters,
            behavior: BehaviorNode, expected_exception=None) -> bool:
        # Steps to run a test case:
        # 1. Get instance of the testing class (Constructor has already been checked
        test_instance = self.java_class_instantiation.instantiate(test_class)

        # 2. Get the current parameters list of the class instance before the execution
        old_variables = self.java_variable_extractor.get_parameters(test_instance, test_class)

        old_duplicate = self.java_duplication_helper.duplicate(test_class, test_instance)

        # 3. execute the method with the parameters
        execution_result = self.test_case_execution.execute_method(test_instance, test_case, consistency_test_case)

        new_variables = self.java_variable_extractor.get_parameters(test_instance, test_class)

        result_parameters = ResultParameters(method_call_parameters=execution_result.parameters,
                                             old_instance_variables=old_variables,
                                             new_instance_variables=new_variables,
                                             csp_parameters=csp_parameters)

        result_instances = ResultInstances(old=old_duplicate, new=test_instance)

        return self.execution_verifier.verify(execution_result=execution_result,
                                              result_parameters=result_parameters,
                                              behavior=behavior,
                                              expected_exception=expected_exception,
                                              consistency_test_case=consistency_test_case,
                                              test_case=test_case,
                                              result_instances=result_instances)
