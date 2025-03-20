from jpype import java


class JavaTypeExtractionInfo:
    def __init__(self, variable_type: str, dimension: int = 0):
        self.variable_type = variable_type
        self.full_variable_type = variable_type if dimension == 0 else f"{variable_type}[]"
        self.dimension = dimension

    def __eq__(self, other):
        if isinstance(other, JavaTypeExtractionInfo):
            return self.variable_type == other.variable_type and self.dimension == other.dimension

        if isinstance(other, str):
            return str(self) == other

        if isinstance(other, java.lang.String):
            return str(self) == other

        return False

    def __str__(self):
        return f"{self.variable_type}{'[]' * self.dimension}"

    def is_array(self) -> bool:
        return self.dimension > 0
