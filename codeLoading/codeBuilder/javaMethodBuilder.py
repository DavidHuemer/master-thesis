from definitions.code.methodExtractionInfo import MethodExtractionInfo
from definitions.javaMethod import JavaMethod
from helper.logs.loggingHelper import LoggingHelper


class JavaMethodBuilder:
    """
    A class to build a Java method out of an extracted method info
    """

    @staticmethod
    def build_java_methods(method_infos: list[MethodExtractionInfo]) -> list[JavaMethod]:
        """
        Builds Java methods out of extracted method infos
        :param method_infos: The extracted method infos
        :return: The Java methods
        """

        methods = []

        for method_info in method_infos:
            if method_info.comment is None:
                LoggingHelper.log_warning(f"Method {method_info.method_name} has no comment")
            else:
                methods.append(JavaMethod(method_info))

        return methods

    @staticmethod
    def build_java_method(method_info: MethodExtractionInfo) -> JavaMethod:
        """
        Builds a Java method out of an extracted method info
        :param method_info: The extracted method info
        :return: The Java method
        """
        return JavaMethod(method_info)
