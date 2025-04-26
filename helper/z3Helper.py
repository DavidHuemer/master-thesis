from definitions.evaluations.csp.cspParameter import CSPParameter


def get_z3_value(param):
    return param.value if isinstance(param, CSPParameter) else param
