import re

from definitions.code.classExtractionInfo import ClassExtractionInfo


class JavaClassReader:
    """
    This class is responsible for reading a java class from a file.
    """

    @staticmethod
    def get_java_class_from_code(file_content):
        """
        This method reads a java class from a file and returns the class information.
        :param file_content: The content of the java file.
        :return: The information of the class.
        """

        class_info_regex = (r"(?:.|\n)*(?P<classProtection>public|private)[\s\n]+class[\s\n]+(?P<className>[A-Z|a-z]["
                            r"A-Z|a-z|\d]+)[\s|\n]+{[\s|\n]*(?P<code>(?:.|\n)+)}")
        class_groups = re.match(class_info_regex, file_content).groupdict()

        if len(class_groups) is not 3:
            raise Exception("Could not find class in code")

        class_groups["code"] = class_groups["code"].strip()
        return ClassExtractionInfo(class_groups["classProtection"], class_groups["className"], class_groups["code"])
