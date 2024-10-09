from codeExecution.vm.VMHelper import VMHelper
from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder

jml_code = (" // @requires arr != null;\n"
            "// @ensures (\\result == -1) <==> (\\forall int i; 0 <= i && i < arr.length; arr[i] != target);\n"
            "// @ensures (\\result != -1) ==> (0 <= \\result && \\result < arr.length && arr[\\result] == target);\n"
            "// @signals (NullPointerException) arr == null;")


def main():
    vm_helper = VMHelper()
    try:
        vm_helper.start()

        code = JavaCodeReader().get_java_from_file("data\\code\\find\\IndexOf.java")
        builder = ConsistencyTestCaseBuilder()
        test_cases = builder.build_test_cases([], [code])

        result = JmlVerifier().verify(test_cases[0], jml_code)

        if result.consistent is None:
            LoggingHelper.log_error(result)
        else:
            LoggingHelper.log_info(result)
    except Exception as e:
        raise e
    finally:
        vm_helper.close()


if __name__ == "__main__":
    main()
