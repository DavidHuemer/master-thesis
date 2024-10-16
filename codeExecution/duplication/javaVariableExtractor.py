from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.evaluations.csp.parameters.instanceVariables import InstanceVariables


class JavaVariableExtractor:
    @staticmethod
    def get_parameters(instance, test_class: JavaRuntimeClass) -> InstanceVariables:
        # TODO: Get the parameters of the instance

        variables = InstanceVariables()

        for field in test_class.get_fields():
            field.setAccessible(True)
            key = field.getName()
            value = field.get(instance)
            variables.add_parameter(key, value)

        # for field in MyClass.class_.getDeclaredFields():

        return variables
