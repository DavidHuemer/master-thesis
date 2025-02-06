import os
from glob import glob

import javalang
from javalang.tree import MethodDeclaration, FormalParameter

from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.code.protectionModifier import ProtectionModifier
from definitions.envKeys import JAVA_FILES
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod
from helper.files.fileReader import FileReader
from helper.logs.loggingHelper import log_info
from util.rattr import rgetattr


def get_java_code_from_directory() -> list[JavaCode]:
    log_info("Getting Java code from directory")
    java_file_paths = get_java_file_paths()

    # with ThreadPoolExecutor() as executor:
    #     results = list(executor.map(get_java_code_from_file, java_file_paths))
    # return results

    return [get_java_code_from_file(java_file) for java_file in java_file_paths]


def get_java_code_from_file(java_file) -> JavaCode:
    return get_java_code_from_content(java_file, FileReader.read(java_file))


def get_java_code_from_content(java_file: str, java_content: str) -> JavaCode:
    tree = javalang.parse.parse(java_content)

    # Get class declaration
    class_declaration = tree.types[0]
    methods: list[MethodDeclaration] = getattr(class_declaration, 'methods', [])

    method_infos = [get_method_info(m) for m in methods]
    return JavaCode(java_file, class_declaration.name, method_infos)


def get_method_info(method: MethodDeclaration) -> JavaMethod:
    return JavaMethod(name=getattr(method, 'name', None),
                      method_protection=get_protection(method),
                      return_type=get_return_type(method),
                      parameters=get_parameters(method),
                      documentation=method.documentation if hasattr(method, 'documentation') else None
                      )


def get_protection(method: MethodDeclaration) -> ProtectionModifier:
    if hasattr(method, 'modifiers'):
        for modifier in method.modifiers:
            if modifier == 'public':
                return ProtectionModifier.PUBLIC
            elif modifier == 'private':
                return ProtectionModifier.PRIVATE
            elif modifier == 'protected':
                return ProtectionModifier.PROTECTED

    return ProtectionModifier.PRIVATE


def get_return_type(method: MethodDeclaration):
    if hasattr(method, 'return_type'):
        return_name = getattr(method.return_type, 'name', None)
        if return_name:
            return_name += '[]' * len(getattr(method.return_type, 'dimensions', []))
        return return_name or 'void'

    return 'void'


def get_parameters(method: MethodDeclaration) -> list[ParameterExtractionInfo]:
    parameters = getattr(method, 'parameters', [])

    return [
        ParameterExtractionInfo(
            name=p.name,
            parameter_type=get_parameter_type(p),
            dimension=len(rgetattr(p, 'type.dimensions', []))
        )
        for p in parameters
    ]


def get_parameter_type(p: FormalParameter):
    return rgetattr(p, 'type.name', None)


def get_java_file_paths():
    path = os.getenv(JAVA_FILES)
    # Check if path is a single file
    if os.path.isfile(path):
        return [path]

    return [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.java'))]
