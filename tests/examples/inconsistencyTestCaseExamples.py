from definitions.inconsistencyTestCase import InconsistencyTestCase
from examples.expectedResultExamples import get_expected_result_example
from examples.javaClassExamples import get_java_code_example
from examples.methodExamples import get_method_example


def get_inconsistency_test_case_example():
    return InconsistencyTestCase(get_java_code_example(), get_method_example(), get_expected_result_example())
