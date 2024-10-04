from definitions.evaluations.csp.parameters.cspParameters import CSPParameters


class CspParamNameGenerator:
    def find_name(self, csp_parameters: CSPParameters, required_name: str) -> str:
        if not csp_parameters.parameter_exists(required_name):
            return required_name
        else:
            return self.find_key_with_index(csp_parameters, required_name, 0)

    def find_key_with_index(self, csp_parameters: CSPParameters, required_name: str, index: int) -> str:
        new_name = f"{required_name}_{index}"
        if not csp_parameters.parameter_exists(new_name):
            return new_name
        else:
            return self.find_key_with_index(csp_parameters, required_name, index + 1)
