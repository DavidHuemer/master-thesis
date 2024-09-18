from codeExecution.runtime.javaClassConstructorHelper import JavaClassConstructorHelper
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


class JavaClassInstantiation:
    """
    Class for instantiating java classes
    """

    def __init__(self, constructor_helper=JavaClassConstructorHelper()):
        """
        Initializes a new JavaClassInstantiation object
        :param constructor_helper: The constructor helper to use
        """
        self.constructor_helper = constructor_helper

    def instantiate(self, clazz: JavaRuntimeClass):
        """
        Instantiates a class
        :param clazz: The class to instantiate
        :return: The instantiated class
        """
        if not self.constructor_helper.has_empty_constructors(clazz):
            raise Exception("No empty constructor found for class")

        return clazz.clazz()
