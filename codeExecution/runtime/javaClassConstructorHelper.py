from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


class JavaClassConstructorHelper:
    """
    Helper class for java class constructors
    """

    @staticmethod
    def has_empty_constructors(clazz: JavaRuntimeClass):
        """
        Returns whether the given class has an empty constructor
        :param clazz: The class to check
        :return: Whether the class has an empty constructor
        """
        return any(len(constructor.getParameterTypes()) == 0 for constructor in clazz.get_constructors())
