from codeExecution.runtime.javaClassInstantiation import instantiate_clazz
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


def duplicate_java_class(test_class: JavaRuntimeClass, instance):
    copy_instance = instantiate_clazz(test_class)

    for field in test_class.get_fields():
        field_name = str(field.getName())
        if hasattr(copy_instance, field_name):
            copy_instance.__setattr__(field_name, field.get(instance))

    return copy_instance
