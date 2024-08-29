from definitions.code.classExtractionInfo import ClassExtractionInfo
from definitions.javaCode import JavaCode
from examples.methodExamples import get_method_extraction_info_example


def get_class_extraction_info() -> ClassExtractionInfo:
    return ClassExtractionInfo("public", "Example", "class Example {\n\n}")


def get_java_code_example() -> JavaCode:
    return JavaCode("path", get_class_extraction_info(), [get_method_extraction_info_example()])
