from definitions.codeExecution.runtime.javaRuntimeParameter import JavaRuntimeParameter


class JavaRuntimeMethod:
    """
    Represents a java method
    """

    def __init__(self, method):
        """
        Initializes a new JavaRuntimeMethod object
        :param method: The jpype method object
        """
        self.method = method
        self.method_name = str(method.getName())
        self.modifiers = method.getModifiers()
        self.return_type = method.getReturnType().getName()
        self.parameters = [JavaRuntimeParameter(param) for param in method.getParameterTypes()]

    def __str__(self):
        return f'{self.return_type} {self.method_name} ({", ".join([str(param) for param in self.parameters])})'
