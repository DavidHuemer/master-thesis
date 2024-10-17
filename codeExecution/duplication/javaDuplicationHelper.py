from codeExecution.runtime.javaClassInstantiation import JavaClassInstantiation
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


class JavaDuplicationHelper:
    def __init__(self, java_class_instantiation=JavaClassInstantiation()):
        self.java_class_instantiation = java_class_instantiation

    def duplicate(self, test_class: JavaRuntimeClass, instance):
        copy_instance = self.java_class_instantiation.instantiate(test_class)

        for field in test_class.get_fields():
            field_name = str(field.getName())
            if hasattr(copy_instance, field_name):
                copy_instance.__setattr__(field_name, field.get(instance))

        return copy_instance
