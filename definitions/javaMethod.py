from definitions.code.javaTypeExtractionInfo import JavaTypeExtractionInfo
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.code.protectionModifier import ProtectionModifier


class JavaMethod:
    def __init__(self, name: str, method_protection: ProtectionModifier, return_type: JavaTypeExtractionInfo,
                 documentation: str,
                 parameters: list[ParameterExtractionInfo]):
        self.name = name
        self.method_protection = method_protection
        self.return_type = return_type
        self.comment = documentation
        self.parameters = parameters

    def __eq__(self, other):
        return (self.return_type == other.return_type
                and self.name == other.name
                and self.comment == other.comment
                and self.parameters == other.parameters)

    def __str__(self):
        return (f"{self.method_protection} {str(self.return_type)} {self.name} "
                f"({', '.join([str(par) for par in self.parameters])})")
