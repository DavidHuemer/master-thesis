from definitions.code.methodExtractionInfo import MethodExtractionInfo
from definitions.javaMethod import JavaMethod


def get_method_extraction_info_example(name="exampleMethod") -> MethodExtractionInfo:
    return MethodExtractionInfo("/**\n* example comment\n*/",
                                "public", "void",
                                name,
                                "(int a, int b)")


def get_method_example(name="exampleMethod") -> JavaMethod:
    return JavaMethod(get_method_extraction_info_example(name=name), [])
