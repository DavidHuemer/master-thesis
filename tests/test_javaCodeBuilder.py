from unittest import TestCase
from unittest.mock import Mock

from codeLoading.codeBuilder.javaCodeBuilder import JavaCodeBuilder
from examples.javaClassExamples import get_class_extraction_info
from examples.methodExamples import get_method_example, get_method_extraction_info_example


class TestJavaCodeBuilder(TestCase):
    def setUp(self):
        self.java_method_builder = Mock()
        self.java_code_builder = JavaCodeBuilder(self.java_method_builder)

    def test_build_java_code(self):
        methods = [get_method_example()]
        self.java_method_builder.build_java_methods.return_value = methods
        class_info = get_class_extraction_info()
        method_infos = [get_method_extraction_info_example()]
        java_code = self.java_code_builder.build_java_code("file_path", class_info, method_infos)

        self.assertEqual(java_code.file_path, "file_path")
        self.assertEqual(java_code.class_info, class_info)
        self.java_method_builder.build_java_methods.assert_called_once_with(method_infos)
        self.assertEqual(java_code.methods, methods)
