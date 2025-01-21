import sys

from dotenv import load_dotenv

from Application import Application
from codeExecution.compilation.javaCompilationRunner import compilation_timer
from codeExecution.runtime.codeExecution import code_execution_timer
from consistencyTestCaseLoading.consistencyTestCaseLoading import get_test_cases, get_test_cases_timer
from definitions.evaluations.csp.jmlProblem import add_solution_constraint_timer
from helper.logs.loggingHelper import log_info
from parser.tree.astGenerator import ast_generator_timer
from pipeline.consistencyPipeline import run_consistency_pipeline, inconsistency_pipeline_timer
from pipeline.jmlVerifier.jmlVerifier import verify_jml_timer
from testGeneration.testCaseGeneration.testCaseGenerator import generate_for_parameter_timer
from testGeneration.testCollections.testCollectionsBuilder import test_collections_build_timer
from testGeneration.testSuiteBuilder import test_suite_generation_timer
from verification.behaviors.behaviorsRunner import behavior_runner_timer
from verification.csp.jmlSolver import solution_generation_timer, add_constraint_timer
from verification.resultVerification.executionVerifier import execution_verifier_timer


def main():
    test_cases = get_test_cases()

    log_info(f"Loaded {len(test_cases)} consistency test cases")

    run_consistency_pipeline(test_cases)

    log_info(f"Getting test cases took: {get_test_cases_timer.timers['get_test_cases']:.6f} seconds")
    log_info(f"Inconsistency pipeline took: {inconsistency_pipeline_timer.timers['run_consistency_pipeline']:.6f} seconds")


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

    #log_info(f"Running the code took: {code_execution_timer.timers['code_execution']:.6f} seconds")
    #log_info(f"Verifying the execution took: {execution_verifier_timer.timers['execution_verifier']:.6f} seconds")


if __name__ == "__main__":
    env_file = f"env/{sys.argv[1]}"

    # set the environment file
    load_dotenv(env_file)

    log_info(f"Using config file {env_file}")

    app = Application()
    app.wire(modules=[sys.modules[__name__]])
    app.pipeline().wire(modules=["pipeline.consistencyPipeline"])
    app.parser().wire(modules=["parser.tree.astGenerator"])
    app.constraints().wire(modules=["testGeneration.constraints.constraintsBuilder"])
    app.test_case_generation().wire(modules=["testGeneration.testCaseGeneration.testCaseGenerator"])
    app.result_verification().wire(modules=["verification.resultVerification.testCaseRunner"])

    main()
