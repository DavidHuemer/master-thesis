from definitions.code.instanceVariable import InstanceVariable
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.parameters.parameters import Parameters
from helper.parameterHelper.parameterGenerator import get_initial_parameter
from helper.parameterHelper.parameterValueGenerator import get_parameter_value_by_python
from testGeneration.testCaseGeneration.javaTypeMapper import get_python_value_from_original_java


def initialize_instance_variables(instance_parameters: Parameters, instance, test_class: JavaRuntimeClass):
    for instance_variable in get_instance_variables(instance, test_class):
        instance_parameter = get_initial_parameter(java_type=instance_variable.variable_type,
                                                   name=instance_variable.name, dimension=0)

        instance_parameter.get_state().parameter_value = get_parameter_value_by_python(instance_variable.value,
                                                                                       instance_variable.variable_type)

        instance_parameters.add_parameter(instance_parameter)


def update_instance_variables(instance_parameters: Parameters, instance, test_class: JavaRuntimeClass):
    for instance_variable in get_instance_variables(instance, test_class):
        parameter_value = get_parameter_value_by_python(instance_variable.value, instance_variable.variable_type)
        instance_parameters[instance_variable.name].update_new(parameter_value)


def get_instance_variables(instance, test_class: JavaRuntimeClass):
    for field in test_class.get_fields():
        field.setAccessible(True)
        field_name = str(field.getName())
        field_type = str(field.getType().getName())

        field_value = get_python_value_from_original_java(field.get(instance))
        yield InstanceVariable(name=field_name, variable_type=field_type, value=field_value)
