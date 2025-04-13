from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.evaluations.csp.parameters.instanceVariables import InstanceVariables


def get_parameters(instance, test_class: JavaRuntimeClass) -> InstanceVariables:
    variables = InstanceVariables()

    for field in test_class.get_fields():
        field.setAccessible(True)
        variables.add_parameter(field.getName(), field.get(instance))

    return variables
