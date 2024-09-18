import jpype

from definitions.codeExecution.runtime.javaRuntimeMethod import JavaRuntimeMethod


class ModifierHelper:
    """
    Helper class for java modifiers.
    Must be used inside a JVM.
    """

    @staticmethod
    def is_public(method: JavaRuntimeMethod):
        """
        Check if the method is public
        :param method: The method that should be checked for being public
        :return: True if the method is public, False otherwise
        """
        modifier_class = jpype.JClass("java.lang.reflect.Modifier")
        return modifier_class.isPublic(method.modifiers)