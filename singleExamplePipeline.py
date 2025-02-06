# class SingleExamplePipeline:
#     def __init__(self, consistency_test_case_loader=ConsistencyTestCaseLoader(),
#                  consistency_pipeline=ConsistencyPipeline(),
#                  statistics_writer=StatisticsWriter()):
#         self.consistency_test_case_loader = consistency_test_case_loader
#         self.consistency_pipeline = consistency_pipeline
#         self.statistics_writer = statistics_writer
#
#     def run(self, name: str):
#         try:
#             LoggingHelper.log_info("Starting main pipeline. (Analyzing JavaDoc consistency)")
#             test_cases = self.consistency_test_case_loader.get_test_cases()
#
#             filtered_test_cases = list(filter(lambda x: x.get_name() == name, test_cases))
#
#             self.consistency_pipeline.setup()
#             results = self.consistency_pipeline.get_results(filtered_test_cases)
#             self.write_statistics(results)
#         except Exception as e:
#             LoggingHelper.log_error(f'Error running main pipeline: {e}')
#             return
#
#     def write_statistics(self, results):
#         try:
#             self.statistics_writer.write(results)
#         except Exception as e:
#             LoggingHelper.log_error(f'Error writing statistics: {e}')
import sys
from webbrowser import get

from codeExecution.compilation.javaCompilationRunner import compile_java_files
from codeExecution.vm.javaVm import is_java_vm_started, start_java_vm
from consistencyTestCaseLoading.consistencyTestCaseLoading import build_test_case
from consistencyTestCaseLoading.expectedResultsLoader import get_expected_results
from consistencyTestCaseLoading.javaCodeLoading import get_java_code_from_file
from helper.files.fileReader import read_file
from helper.logs.loggingHelper import log_info
from pipeline.consistencyResultGetter import ConsistencyResultGetter
from util.envUtil import load_and_check_env_file


def single_example_pipeline():
    content = read_file("data/example-jml.txt")

    # split the content by a line that contains ----------
    # There should be two parts (string) the one before the line and the one after the line
    java_file, content = content.split("----------")

    # trim the content
    java_file = java_file.strip()
    content = content.strip()

    compile_java_files([java_file])

    print("")
    java_code = get_java_code_from_file(java_file)
    test_case = build_test_case(java_code, java_code.methods[0], get_expected_results())

    print(test_case)

    if not is_java_vm_started():
        start_java_vm()

    result = ConsistencyResultGetter().get_result_by_jml(test_case, content)
    log_info(str(result))


if __name__ == '__main__':
    load_and_check_env_file(sys.argv[1])
    single_example_pipeline()
