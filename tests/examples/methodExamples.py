from definitions.code.methodExtractionInfo import MethodExtractionInfo


def get_method_extraction_info_example() -> MethodExtractionInfo:
    return MethodExtractionInfo("/**\n* example comment\n*/",
                                "public", "void",
                                "exampleMethod",
                                "(int a, int b)")
