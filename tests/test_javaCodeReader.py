from unittest import TestCase
from unittest.mock import Mock

from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from examples.javaClassExamples import get_class_extraction_info, get_java_code_example
from examples.methodExamples import get_method_extraction_info_example


class TestJavaCodeReader(TestCase):
    def setUp(self):
        self.file_reader = Mock()
        self.class_reader = Mock()
        self.java_method_reader = Mock()
        self.java_code_builder = Mock()
        self.java_code_reader = JavaCodeReader(self.file_reader, self.class_reader,
                                               self.java_method_reader, self.java_code_builder)

    def test_get_java_from_file(self):
        java_code = get_java_code_example()
        class_extraction_info = get_class_extraction_info()
        methods = [get_method_extraction_info_example()]

        self.file_reader.read.return_value = "content"
        self.class_reader.get_java_class_from_code.return_value = class_extraction_info
        self.java_method_reader.get_methods_from_code.return_value = methods
        self.java_code_builder.build_java_code.return_value = java_code

        result = self.java_code_reader.get_java_from_file("path")
        self.assertEqual(result, java_code)
        self.file_reader.read.assert_called_once_with("path")
        self.class_reader.get_java_class_from_code.assert_called_once_with("content")
        self.java_method_reader.get_methods_from_code.assert_called_once_with(class_extraction_info.code)
        self.java_code_builder.build_java_code.assert_called_once_with("path", class_extraction_info, methods)
