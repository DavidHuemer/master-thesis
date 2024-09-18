from definitions.code.methodExtractionInfo import MethodExtractionInfo
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo


class JavaMethod:
    def __init__(self, method_info: MethodExtractionInfo, parameters: list[ParameterExtractionInfo]):
        self.return_type = method_info.method_return_type
        self.name = method_info.method_name
        self.comment = method_info.comment
        self.parameters = method_info.method_parameters
        self.parameters_list = parameters

    def __eq__(self, other):
        return (self.return_type == other.return_type
                and self.name == other.name
                and self.comment == other.comment
                and self.parameters == other.parameters)
