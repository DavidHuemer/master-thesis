import sys

from consistencyTestCaseLoading.consistencyTestCaseLoading import get_test_cases, get_test_cases_timer
from helper.logs.loggingHelper import log_info
from pipeline.consistencyPipeline import run_consistency_pipeline, inconsistency_pipeline_timer
from statistics.statisticsWriter import write_statistics
from util.envUtil import load_and_check_env_file


def main():
    test_cases = get_test_cases()
    log_info(f"Loaded {len(test_cases)} consistency test cases")

    results = run_consistency_pipeline(test_cases)

    write_statistics(results)
    log_info(f"Getting test cases took: {get_test_cases_timer.timers['get_test_cases']:.6f} seconds")
    log_info(
        f"Inconsistency pipeline took: {inconsistency_pipeline_timer.timers['run_consistency_pipeline']:.6f} seconds")

    # log_info(f"Verifying jml took: {verify_jml_timer.timers['verify_jml']:.6f} seconds")
    # log_info(f"Generation of test suites took: {test_suite_generation_timer.timers['get_test_suite']:.6f} seconds")
    # log_info(f"Generation AST took: {ast_generator_timer.timers['ast_generator']:.6f} seconds")
    # log_info(
    #     f"Generation of test collections took: {test_collections_build_timer.timers['build_test_collections']:.6f} seconds")
    # log_info(
    #     f"Generation of test cases by parameter constraints took: {generate_for_parameter_timer.timers['generate_for_parameter']:.6f} seconds")
    # log_info(f"Generation of solutions took: {solution_generation_timer.timers['solution_generation']:.6f} seconds")
    # log_info(
    #     f"Adding solution constraint took: {add_solution_constraint_timer.timers['add_solution_constraint']:.6f} seconds")
    #
    # log_info(f"Adding constraints took: {add_constraint_timer.timers['add_constraint']:.6f} seconds")
    # log_info(f"Compilation took: {compilation_timer.timers['compilation']:.6f} seconds")
    #
    # log_info(f"Running behaviors took: {behavior_runner_timer.timers['run_behaviors']:.6f} seconds")

    # log_info(f"Running the code took: {code_execution_timer.timers['code_execution']:.6f} seconds")
    # log_info(f"Verifying the execution took: {execution_verifier_timer.timers['execution_verifier']:.6f} seconds")


if __name__ == "__main__":
    # Load the environment file
    load_and_check_env_file(sys.argv[1])

    # app = Application()
    # app.wire(modules=[sys.modules[__name__]])
    # app.pipeline().wire(modules=["pipeline.consistencyPipeline"])
    # app.parser().wire(modules=["parser.tree.astGenerator"])
    # app.constraints().wire(modules=["testGeneration.constraints.constraintsBuilder"])
    # app.test_case_generation().wire(modules=["testGeneration.testCaseGeneration.testCaseGenerator"])
    # app.result_verification().wire(modules=["verification.resultVerification.testCaseRunner"])

    main()
