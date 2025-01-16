from codeExecution.runtime.modifierHelper import is_public
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.codeExecution.runtime.javaRuntimeMethod import JavaRuntimeMethod
from definitions.evaluations.tests.testSuite import TestSuite
from definitions.javaMethod import JavaMethod


def has_correct_method(java_class: JavaRuntimeClass, test_suite: TestSuite):
    """
    Check if the java class has the correct method
    :param java_class: The java class extracted via java reflection
    :param test_suite: The test suite with the method that should be tested
    :return: True if the method is correct, False otherwise
    """

    for method in java_class.get_methods():
        if is_method_correct(method, test_suite.consistency_test_case.method_info):
            return True

    return False


def is_method_correct(method: JavaRuntimeMethod, method_info: JavaMethod):
    """
    Check if the method is correct (the method is the same as the method that should be tested)
    :param method: The method extracted via java reflection
    :param method_info: The method that should be tested
    :return: True if the method is correct, False otherwise
    """

    # Check if the method has the correct name
    if not method.method_name == method_info.name:
        return False

    # Check if the method is public
    if not is_public(method):
        return False

    # Check if the method has the correct return type
    if not method.return_type == method_info.return_type:
        return False

    for i in range(len(method.parameters)):
        if not method.parameters[i].parameter_name == method_info.parameters[i].parameter_type:
            return False

    return True
