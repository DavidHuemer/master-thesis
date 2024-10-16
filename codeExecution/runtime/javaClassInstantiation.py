from codeExecution.runtime.javaClassConstructorHelper import JavaClassConstructorHelper
from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


class JavaClassInstantiation:
    """
    Class for instantiating java classes
    """

    def __init__(self):
        """
        Initializes a new JavaClassInstantiation object
        """

    @staticmethod
    def instantiate(clazz: JavaRuntimeClass):
        """
        Instantiates a class
        :param clazz: The class to instantiate
        :return: The instantiated class
        """
        return clazz.clazz()
