from codeExecution.vm.VMHelper import VMHelper
from codeLoading.codeReader.javaCodeReader import JavaCodeReader
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from testCases.consistencyTestCaseBuilder import ConsistencyTestCaseBuilder

jml_code = ("//@ requires length >= 0;\n"
            "//@ ensures \\result.length() == length;\n"
            "//@ ensures (\\forall int i; 0 <= i && i < length; 'a' <= \\result.charAt(i) && \\result.charAt(i) <= 'z');\n"
            "//@ ensures (\\forall int i; 0 <= i && i < length; \\result.charAt(i) == 'a' + i % 26);")


def main():
    vm_helper = VMHelper()
    try:
        vm_helper.start()

        code = JavaCodeReader().get_java_from_file("data\\code\\compute\\GenerateString.java")
        builder = ConsistencyTestCaseBuilder()
        test_cases = builder.build_test_cases([], [code])

        jml_verifier = JmlVerifier()
        jml_verifier.setup()
        result = jml_verifier.verify(test_cases[0], jml_code)

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
