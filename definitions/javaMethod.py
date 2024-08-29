from definitions.code.methodExtractionInfo import MethodExtractionInfo


class JavaMethod:
    def __init__(self, method_info: MethodExtractionInfo):
        self.comment = method_info.comment
