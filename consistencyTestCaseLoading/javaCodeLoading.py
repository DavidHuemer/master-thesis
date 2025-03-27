import os
from glob import glob

import javalang
from javalang.tree import MethodDeclaration, FormalParameter, CompilationUnit, ClassDeclaration

from definitions.code.javaTypeExtractionInfo import JavaTypeExtractionInfo
from definitions.code.parameterExtractionInfo import ParameterExtractionInfo
from definitions.code.protectionModifier import ProtectionModifier
from definitions.envKeys import JAVA_FILES
from definitions.javaCode import JavaCode
from definitions.javaMethod import JavaMethod
from helper.files.fileReader import FileReader
from helper.logs.loggingHelper import log_info, log_error
from util.rattr import rgetattr


def get_java_code_from_directory() -> list[JavaCode]:
    log_info("Getting Java code from directory")
    java_file_paths = get_java_file_paths()

    # with ThreadPoolExecutor() as executor:
    #     results = list(executor.map(get_java_code_from_file, java_file_paths))
    # return results

    return [code for java_file in java_file_paths if (code := get_java_code_from_file(java_file)) is not None]


def get_java_code_from_file(java_file_path: str) -> JavaCode | None:
    try:
        return get_java_code_from_content(java_file_path, FileReader.read(java_file_path))
    except Exception as e:
        log_error(f"Error reading file {java_file_path}: {e}")
        return None


def get_java_code_from_content(java_file: str, java_content: str) -> JavaCode | None:
    tree: CompilationUnit = javalang.parse.parse(java_content)
    class_declaration: ClassDeclaration = tree.types[0] if hasattr(tree, 'types') else None
    methods: list[MethodDeclaration] = getattr(class_declaration, 'methods', [])

    method_infos: list[JavaMethod] = [get_method_info(m) for m in methods]
    return JavaCode(file_path=java_file, class_name=getattr(class_declaration, 'name', None), methods=method_infos)


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


def get_return_type(method: MethodDeclaration) -> JavaTypeExtractionInfo:
    if hasattr(method, 'return_type'):
        return_name = getattr(method.return_type, 'name', 'void')
        dimension = 0 if return_name == 'void' else len(getattr(method.return_type, 'dimensions', []))
        return JavaTypeExtractionInfo(return_name, dimension)

    return JavaTypeExtractionInfo('void')


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
    return [path] if os.path.isfile(path) else glob(os.path.join(path, '**', '*.java'), recursive=True)
