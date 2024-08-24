from unittest import TestCase

from codeLoading.codeReader.javaMethodReader import JavaMethodReader
from definitions.code.methodExtractionInfo import MethodExtractionInfo


def get_method_info(comment: str | None = "/**\n * Comment\n */", publicity="public", return_value="void",
                    method_name="method", parameterlist="()"):
    return MethodExtractionInfo(comment, publicity, return_value, method_name, parameterlist)


class TestJavaMethodReader(TestCase):
    def test_get_methods_from_code_for_empty_class(self):
        self.assertEqual([], JavaMethodReader.get_methods_from_code(""))

    def test_get_methods_from_code_for_one_method_without_comment(self):
        code = "public void method() {}"
        method_info = get_method_info(comment=None)
        self.assertEqual([method_info], JavaMethodReader.get_methods_from_code(code))

    def test_get_methods_from_code_for_one_method_with_comment(self):
        code = "/**\n * Comment\n */\npublic void method() {}"
        method_info = get_method_info()
        self.assertEqual([method_info], JavaMethodReader.get_methods_from_code(code))

    def test_get_methods_from_code_for_two_methods(self):
        code = "public void method1() {}\npublic void method2() {}"
        method_info1 = get_method_info(comment=None, method_name="method1")
        method_info2 = get_method_info(comment=None, method_name="method2")
        self.assertEqual([method_info1, method_info2], JavaMethodReader.get_methods_from_code(code))

    def test_get_methods_from_code_for_two_methods_with_comments(self):
        code = "/**\n * Comment\n */\npublic void method1() {}\n/**\n * Comment\n */\npublic void method2() {}"
        method_info1 = get_method_info(method_name="method1")
        method_info2 = get_method_info(method_name="method2")
        self.assertEqual([method_info1, method_info2], JavaMethodReader.get_methods_from_code(code))
