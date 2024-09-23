from codeExecution.runtime.javaClassInstantiation import JavaClassInstantiation
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


class JavaDuplicationHelper:
    def __init__(self, java_class_instantiation=JavaClassInstantiation()):
        self.java_class_instantiation = java_class_instantiation

    def duplicate(self, test_class: JavaRuntimeClass, instance):
        copy_instance = self.java_class_instantiation.instantiate(test_class)

        # TODO: Set variables of the instance to the copy_instance
        return copy_instance
