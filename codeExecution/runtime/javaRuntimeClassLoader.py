import jpype

from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.javaCode import JavaCode


def get_class(java_code: JavaCode) -> JavaRuntimeClass:
    clazz = jpype.JClass(java_code.class_name)
    return JavaRuntimeClass(clazz)
