from helper.logs.loggingHelper import LoggingHelper
from pipeline.consistencyPipeline import ConsistencyPipeline
from statistics.statisticsWriter import StatisticsWriter
from testCases.consistencyTestCaseLoader import ConsistencyTestCaseLoader


class MainPipeline:
    def __init__(self, consistency_test_case_loader=ConsistencyTestCaseLoader(),
                 consistency_pipeline=ConsistencyPipeline(),
                 statistics_writer=StatisticsWriter()):
        self.consistency_test_case_loader = consistency_test_case_loader
        self.consistency_pipeline = consistency_pipeline
        self.statistics_writer = statistics_writer

    def run(self):
        try:
            LoggingHelper.log_info("Starting main pipeline. (Analyzing JavaDoc consistency)")
            test_cases = self.consistency_test_case_loader.get_test_cases()

            self.consistency_pipeline.setup()
            results = self.consistency_pipeline.get_results(test_cases)
            self.write_statistics(results)
        except Exception as e:
            LoggingHelper.log_error(f'Error running main pipeline: {e}')
            return

    def write_statistics(self, results):
        try:
            self.statistics_writer.write(results)
        except Exception as e:
            LoggingHelper.log_error(f'Error writing statistics: {e}')
