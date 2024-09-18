import jpype

from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass
from definitions.javaCode import JavaCode


class JavaRuntimeClassLoader:
    """
    Helper method for loading java classes during runtime
    Must be executed inside a JVM
    """

    @staticmethod
    def get_class(java_code: JavaCode) -> JavaRuntimeClass:
        clazz = jpype.JClass(java_code.class_info.class_name)
        return JavaRuntimeClass(clazz)
