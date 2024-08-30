from definitions.code.methodExtractionInfo import MethodExtractionInfo


class JavaMethod:
    def __init__(self, method_info: MethodExtractionInfo):
        self.name = method_info.method_name
        self.comment = method_info.comment

    def __eq__(self, other):
        return self.name == other.name and self.comment == other.comment
