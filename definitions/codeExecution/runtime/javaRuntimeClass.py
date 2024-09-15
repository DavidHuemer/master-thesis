import jpype

from definitions.codeExecution.runtime.javaRuntimeMethod import JavaRuntimeMethod


class JavaRuntimeClass:
    """
    Represents a java class. Not an instance of it
    """

    def __init__(self, clazz: jpype.JClass):
        """
        Initializes a new JavaRuntimeClass object
        :param clazz: The jpype class object
        """
        self.clazz = clazz

    def get_constructors(self):
        """
        Returns all constructors of the class
        :return: The constructors of the class
        """
        return self.clazz.class_.getConstructors()

    def get_methods(self) -> list[JavaRuntimeMethod]:
        """
        Returns all methods of the class
        :return: The methods of the class
        """
        return [JavaRuntimeMethod(method) for method in
                self.clazz.class_.getMethods()]
