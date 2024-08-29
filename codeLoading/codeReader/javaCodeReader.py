from codeLoading.codeBuilder.javaCodeBuilder import JavaCodeBuilder
from codeLoading.codeReader.javaClassReader import JavaClassReader
from codeLoading.codeReader.javaMethodReader import JavaMethodReader
from definitions.javaCode import JavaCode
from helper.files.fileReader import FileReader


class JavaCodeReader:
    """
    This class is responsible for reading Java code from a file
    """

    def __init__(self, file_reader=FileReader, class_reader=JavaClassReader, method_reader=JavaMethodReader,
                 java_code_builder=JavaCodeBuilder()):
        self.file_reader = file_reader
        self.class_reader = class_reader
        self.java_method_reader = method_reader
        self.java_code_builder = java_code_builder

    def get_java_from_file(self, file_path) -> JavaCode:
        """
        Returns the Java code from the given file path
        :param file_path: The file path to the Java file
        :return: The Java code
        """

        # First, get the content of the file via the file_reader
        content = self.file_reader.read(file_path)
        class_info = self.class_reader.get_java_class_from_code(content)
        methods = self.java_method_reader.get_methods_from_code(class_info.code)

        return self.java_code_builder.build_java_code(file_path, class_info, methods)
