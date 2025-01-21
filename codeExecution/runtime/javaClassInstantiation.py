from definitions.codeExecution.runtime.javaRuntimeClass import JavaRuntimeClass


def instantiate_clazz(clazz: JavaRuntimeClass):
    """
    Instantiates a class
    :param clazz: The class to instantiate
    :return: The instantiated class
    """
    return clazz.clazz()
