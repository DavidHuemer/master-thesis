from codeLoading.codeBuilder.javaMethodBuilder import JavaMethodBuilder
from definitions.code.classExtractionInfo import ClassExtractionInfo
from definitions.code.methodExtractionInfo import MethodExtractionInfo
from definitions.javaCode import JavaCode


class JavaCodeBuilder:
    """
    Class that builds Java code out of class and method extraction infos
    """

    def __init__(self, java_method_builder=JavaMethodBuilder):
        """
        Initializes the JavaCodeBuilder
        :param java_method_builder: Builder for Java methods
        """
        self.java_method_builder = java_method_builder

    def build_java_code(self, file_path: str, class_info: ClassExtractionInfo,
                        method_infos: list[MethodExtractionInfo]) -> JavaCode:
        """
        Builds Java code out of class and method extraction infos
        :param file_path: The file path of the Java file
        :param class_info: The extracted class info
        :param method_infos: The extracted method infos
        :return: The Java code that was built
        """

        # First build the real methods
        methods = self.java_method_builder.build_java_methods(method_infos)

        return JavaCode(file_path, class_info, methods)
