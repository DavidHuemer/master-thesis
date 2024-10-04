from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters


class CspFunctionNameGenerator:
    def get_name(self, jml_parameters: JmlParameters, required_name: str = 'f'):
        # Check if required_name is already in use (require_name is in functions list)
        if required_name not in jml_parameters.functions:
            return required_name
        else:
            return self.get_name_with_index(jml_parameters, required_name, 0)

    def get_name_with_index(self, jml_parameters: JmlParameters, required_name: str, index: int):
        new_name = f"{required_name}_{index}"
        if new_name not in jml_parameters.functions:
            return new_name
        else:
            return self.get_name_with_index(jml_parameters, required_name, index + 1)
