import os
from glob import glob

import javalang
from javalang.tree import MethodDeclaration, FormalParameter

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod
from helper.files.fileReader import FileReader
from helper.logs.loggingHelper import log_info


def get_java_code_from_directory():
    log_info("Getting Java code from directory")
    java_file_paths = get_java_file_paths()

    # with ThreadPoolExecutor() as executor:
    #     results = list(executor.map(get_java_code_from_file, java_file_paths))
    # return results

    return [get_java_code_from_file(java_file) for java_file in java_file_paths]


def get_java_code_from_file(java_file) -> JavaCode:
    java_content = FileReader.read(java_file)
    return get_java_code_from_content(java_file, java_content)


def get_java_code_from_content(java_file: str, java_content: str) -> JavaCode:
    tree = javalang.parse.parse(java_content)

    # Get class declaration
    class_declaration = tree.types[0]
    methods: list[MethodDeclaration] = class_declaration.methods

    method_infos = [get_method_info(m) for m in methods]
    return JavaCode(java_file, class_declaration.name, method_infos)


def get_method_info(method: MethodDeclaration) -> JavaMethod:
    return JavaMethod(name=method.name if hasattr(method, 'name') else None,
                      method_protection=get_protection(method),
                      return_type=get_return_type(method),
                      parameters=get_parameters(method),
                      comment=method.documentation if hasattr(method, 'documentation') else None
                      )


def get_protection(method: MethodDeclaration) -> str:
    if hasattr(method, 'modifiers'):
        for modifier in method.modifiers:
            if modifier == 'public':
                return 'public'
            elif modifier == 'private':
                return 'private'
            elif modifier == 'protected':
                return 'protected'

    return 'private'


def get_return_type(method: MethodDeclaration):
    if hasattr(method, 'return_type'):
        return_name = getattr(method.return_type, 'name', None)
        if return_name:
            return_name += '[]' * len(getattr(method.return_type, 'dimensions', []))
        return return_name or 'void'

    return 'void'


def get_parameters(method: MethodDeclaration) -> list[ParameterExtractionInfo]:
    parameters = method.parameters if hasattr(method, 'parameters') else []

    return [
        ParameterExtractionInfo(
            name=p.name,
            parameter_type=get_parameter_type(p)
        )
        for p in parameters
    ]


def get_parameter_type(p: FormalParameter):
    param_type = p.type if hasattr(p, 'type') else None

    param_name = param_type.name if hasattr(param_type, 'name') else None

    if param_name is not None and hasattr(param_type, 'dimensions'):
        param_name += '[]' * len(param_type.dimensions)

    return param_name


def get_java_file_paths():
    return [y for x in os.walk('data/code') for y in glob(os.path.join(x[0], '*.java'))]
