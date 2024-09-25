from codeExecution.vm.VMHelper import VMHelper
from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder

jml_code = ("//@requires a != null\n"
            "//@requires a.length == 0 ==> \\result == -1;\n"
            "//@requires a.length > 0 ==> (\\forall int i; 0 <= i && i < a.length; \\result >= a[i]) && (\\exists int j; 0 <= j && j < a.length; \\result == a[j]);")


def main():
    vm_helper = VMHelper()
    try:
        vm_helper.start()

        code = JavaCodeReader().get_java_from_file("data\\code\\max\\BiggestIndex.java")
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
