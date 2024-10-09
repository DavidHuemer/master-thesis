from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


class CspParamNameGenerator:
    def find_name(self, parameters: BaseParameters, required_name: str) -> str:
        if not parameters.parameter_exists(required_name):
            return required_name
        else:
            return self.find_key_with_index(parameters, required_name, 0)

    def find_key_with_index(self, csp_parameters: BaseParameters, required_name: str, index: int) -> str:
        new_name = f"{required_name}_{index}"
        if not csp_parameters.parameter_exists(new_name):
            return new_name
        else:
            return self.find_key_with_index(csp_parameters, required_name, index + 1)
