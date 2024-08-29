from definitions.code.methodExtractionInfo import MethodExtractionInfo
from definitions.javaMethod import JavaMethod


def get_method_extraction_info_example() -> MethodExtractionInfo:
    return MethodExtractionInfo("/**\n* example comment\n*/",
                                "public", "void",
                                "exampleMethod",
                                "(int a, int b)")


def get_method_example() -> JavaMethod:
    return JavaMethod(get_method_extraction_info_example())
