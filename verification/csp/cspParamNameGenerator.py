from definitions.evaluations.csp.parameters.baseParameters import BaseParameters


def find_csp_name(parameters: BaseParameters, required_name: str) -> str:
    if not parameters.parameter_exists(required_name):
        return required_name
    else:
        return find_key_with_index(parameters, required_name, 0)


def find_key_with_index(csp_parameters: BaseParameters, required_name: str, index: int) -> str:
    if index == 100:
        raise Exception(f"Could not find a unique name for {required_name}")

    new_name = f"{required_name}_{index}"
    if not csp_parameters.parameter_exists(new_name):
        return new_name
    else:
        return find_key_with_index(csp_parameters, required_name, index + 1)
