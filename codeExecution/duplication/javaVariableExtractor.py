from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.evaluations.csp.parameters.instanceVariables import InstanceVariables
from definitions.parameters.parameters import Parameters


def get_parameters(instance, test_class: JavaRuntimeClass) -> list[Parameters]:
    parameters = []
    # TODO: Go through fields of instance
    return parameters

    # instance_parameters = Parameters()
    #
    # for field in test_class.get_fields():
    #     field.setAccessible(True)
    #     instance_parameters.add_parameter(field.getName(), field.get(instance))
    #
    # return instance_parameters
