from codeExecution.vm.VMHelper import VMHelper
from definitions import config
from definitions.consistencyTestCase import ConsistencyTestCase
from definitions.evaluations.tests.exceptions.noTestCasesException import NoTestCasesException
from definitions.parser.parserException import ParserException
from definitions.verification.verificationResult import VerificationResult
from helper.logs.loggingHelper import LoggingHelper
from pipeline.jmlGenerator.jmlGenerator import JmlGenerator
from pipeline.jmlVerifier.jmlVerifier import JmlVerifier
from verification.result.verificationResultFactory import VerificationResultFactory


class ConsistencyPipeline:
    """
    Class that is responsible for running the pipeline that finds inconsistencies in the java doc.
    """

    def __init__(self, jml_generator=JmlGenerator(), jml_verifier=JmlVerifier(), vm_helper=VMHelper()):
        self.jml_generator = jml_generator
        self.jml_verifier = jml_verifier
        self.vm_helper = vm_helper
        self.retries = 0

    def get_results(self, consistency_tests: list[ConsistencyTestCase]) -> list[VerificationResult]:
        try:
            LoggingHelper.log_info("Starting consistency pipeline")
            self.vm_helper.start()
            return [self.get_result(test_case) for test_case in consistency_tests]
        except Exception as e:
            # Only to close the VM even if an exception occurs
            raise e
        finally:
            self.vm_helper.close()

    def get_result(self, consistency_test: ConsistencyTestCase) -> VerificationResult:
        try:
            LoggingHelper.log_info(f"Getting result for {consistency_test.get_name()}")

            # Reset the JML generator
            self.jml_generator.reset()

            # First, get initial JML
            jml_code = self.jml_generator.get_from_test_case(consistency_test)
            return self.get_result_by_jml(consistency_test, jml_code)
        except Exception as e:
            return VerificationResultFactory.by_exception(consistency_test, e)
        finally:
            self.retries = 0
            LoggingHelper.log_info("=====================================", show_level=False)

    def get_result_by_jml(self, consistency_test: ConsistencyTestCase, jml_code: str):
        try:
            LoggingHelper.log_debug("JMl code: \n" + jml_code.strip())
            result = self.jml_verifier.verify(consistency_test, jml_code)
            if result.consistent is True:
                return result

            if self.retries >= config.MAX_PIPELINE_TRIES:
                return result

            new_jml = self.jml_generator.get_from_failing_verification(result)
            self.retries += 1
            return self.get_result_by_jml(consistency_test, new_jml)

        except ParserException as parser_exception:
            return self.parser_exception_occurred(parser_exception, consistency_test)
        except NoTestCasesException as e:
            return self.no_test_cases_exception_occurred(e, consistency_test)

    def parser_exception_occurred(self, parser_exception: ParserException, consistency_test: ConsistencyTestCase):
        LoggingHelper.log_warning(f"Parser exception occurred")
        if self.retries >= config.MAX_PIPELINE_TRIES:
            LoggingHelper.log_warning(f"Max retries reached")
            return VerificationResultFactory.by_exception(consistency_test, parser_exception)

        LoggingHelper.log_info("Generating new JML")
        new_jml = self.jml_generator.get_from_parser_exception(consistency_test, parser_exception)
        self.retries += 1
        return self.get_result_by_jml(consistency_test, new_jml)

    def no_test_cases_exception_occurred(self, exception, consistency_test: ConsistencyTestCase):
        LoggingHelper.log_warning(f"No test cases exception occurred")
        if self.retries >= config.MAX_PIPELINE_TRIES:
            return VerificationResultFactory.by_exception(consistency_test, exception)

        new_jml = self.jml_generator.get_from_no_test_cases()
        self.retries += 1
        return self.get_result_by_jml(consistency_test, new_jml)

    def setup(self):
        LoggingHelper.log_info("Setting up consistency pipeline")
        self.jml_generator.setup()
