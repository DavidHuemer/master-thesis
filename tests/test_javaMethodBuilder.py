from unittest import TestCase

from codeLoading.codeBuilder.javaMethodBuilder import JavaMethodBuilder
from examples.methodExamples import get_method_extraction_info_example


class TestJavaMethodBuilder(TestCase):
    def test_build_java_methods_with_empty_array(self):
        methods = JavaMethodBuilder.build_java_methods([])
        self.assertEqual(methods, [])

    def test_build_java_methods_with_one_method(self):
        method_info = get_method_extraction_info_example()

        methods = JavaMethodBuilder.build_java_methods([method_info])
        self.assertEqual(len(methods), 1)
        self.assertEqual(methods[0].comment, method_info.comment)

    def test_build_java_methods_with_one_method_without_comment(self):
        method_info = get_method_extraction_info_example()
        method_info.comment = None

        methods = JavaMethodBuilder.build_java_methods([method_info])
        self.assertEqual(len(methods), 0)

    def test_build_java_methods_with_two_methods(self):
        method_info = get_method_extraction_info_example()

        methods = JavaMethodBuilder.build_java_methods([method_info, method_info])
        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].comment, method_info.comment)
        self.assertEqual(methods[1].comment, method_info.comment)

    def test_build_java_method(self):
        method_info = get_method_extraction_info_example()

        method = JavaMethodBuilder.build_java_method(method_info)
        self.assertEqual(method.comment, method_info.comment)
