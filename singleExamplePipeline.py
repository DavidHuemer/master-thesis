from helper.logs.loggingHelper import LoggingHelper
from pipeline.consistencyPipeline import ConsistencyPipeline
from statistics.statisticsWriter import StatisticsWriter
from consistencyTestCaseLoading.consistencyTestCaseLoader import ConsistencyTestCaseLoader


class SingleExamplePipeline:
    def __init__(self, consistency_test_case_loader=ConsistencyTestCaseLoader(),
                 consistency_pipeline=ConsistencyPipeline(),
                 statistics_writer=StatisticsWriter()):
        self.consistency_test_case_loader = consistency_test_case_loader
        self.consistency_pipeline = consistency_pipeline
        self.statistics_writer = statistics_writer

    def run(self, name: str):
        try:
            LoggingHelper.log_info("Starting main pipeline. (Analyzing JavaDoc consistency)")
            test_cases = self.consistency_test_case_loader.get_test_cases()

            filtered_test_cases = list(filter(lambda x: x.get_name() == name, test_cases))

            self.consistency_pipeline.setup()
            results = self.consistency_pipeline.get_results(filtered_test_cases)
            self.write_statistics(results)
        except Exception as e:
            LoggingHelper.log_error(f'Error running main pipeline: {e}')
            return

    def write_statistics(self, results):
        try:
            self.statistics_writer.write(results)
        except Exception as e:
            LoggingHelper.log_error(f'Error writing statistics: {e}')


if __name__ == '__main__':
    SingleExamplePipeline().run("DigitRoot.digitRoot")
