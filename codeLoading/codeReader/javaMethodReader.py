import re

from definitions.code.methodExtractionInfo import MethodExtractionInfo


class JavaMethodReader:
    """
    This class is responsible for reading the methods of a java file.
    """

    @staticmethod
    def get_methods_from_code(code):
        """
        This method reads the methods from a java file and returns the method information.
        :param code: The content of the java file (without the surrounding class).
        :return: The information of the methods.
        """

        method_regex = (
            r"(?P<comment>/\*{2}(?:\n|.)+?\*/)*(?:\n|\s)*(?P<publicity>public|protected|private)(?:\s|\n)+("
            r"?P<returnValue>[A-Z|a-z][A-Z|a-z|\d\[\]]+)(?:\s|\n)+(?P<methodName>[A-Z|a-z][A-Z|a-z|\d]+)("
            r"?P<parameterlist>\((?:.|\n)*?\))")

        methods = []

        for match in re.finditer(method_regex, code):
            method_group_result = match.groupdict()
            method_info = MethodExtractionInfo(
                method_group_result["comment"],
                method_group_result["publicity"],
                method_group_result["returnValue"],
                method_group_result["methodName"],
                method_group_result["parameterlist"]
            )

            methods.append(method_info)

        return methods
