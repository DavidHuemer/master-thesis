import sys

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import start_java_vm
from consistencyTestCaseLoading.consistencyTestCaseLoading import get_test_cases
from helper.logs.loggingHelper import log_info, log_error
from pipeline.jmlVerifier.jmlVerifier import verify_jml
from util.envUtil import load_and_check_env_file


def main_test():
    test_cases = get_test_cases()

    test_case = [test_case for test_case in test_cases if
                 test_case.java_code.class_name == "StringConcat"]

    if len(test_case) == 0:
        log_error("No test case found")
        return

    test_case = test_case[0]

    compile_java_files([test_case.java_code.file_path])

    with open("jml.txt", "r") as f:
        jml_code = f.read()
        start_java_vm()
        result = verify_jml(test_case, jml_code)


if __name__ == "__main__":
    log_info("Starting test")
    load_and_check_env_file(sys.argv[1])
    main_test()
