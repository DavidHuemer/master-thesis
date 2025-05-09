import re
import time

from definitions.consistencyTestCase import ConsistencyTestCase
from helper.files.fileReader import FileReader


def main():
    content = FileReader.read("data\\examples\\verification_examples.txt")
    files_arr = split(content, '=')
    vm_helper = VMHelper()

    try:
        vm_helper.start()

        for file in files_arr:
            run_file(file)
    except Exception as e:
        LoggingHelper.log_error(e)
    finally:
        vm_helper.close()


def run_file(file: str):
    # method info is first line
    file = file.strip()
    method_info_str = file.split('\n')[0]
    method_info_parts = method_info_str.split(';')

    LoggingHelper.log_info(f"Running file: {method_info_parts[0]}")

    code = JavaCodeReader().get_java_from_file(method_info_parts[0])
    builder = ConsistencyTestCaseBuilder()
    test_cases = builder.build_test_cases([], [code])

    # the jml part is every line after the first line
    jml_part = '\n'.join(file.split('\n')[1:])
    jml_arr = split(jml_part, '-')

    for jml in jml_arr:
        run_jml(jml, test_cases[0])

    # result = JmlVerifier().verify(test_cases[0], "")
    # result = JmlVerifier().verify(test_cases[0], jml_code)


def run_jml(jml_with_result: str, test_case):
    # The jml part is every line until the line starts with result:
    jml_lines = jml_with_result.split('\n')

    # Join jml lines until the line starts with result:
    jml = ''
    result_index = -1
    for line in jml_lines:
        if line.startswith('result:'):
            result_index = jml_lines.index(line)
            break
        jml += line + '\n'

    if result_index == -1:
        LoggingHelper.log_error("No expected result found")
        result = "true"
    else:
        result_line = jml_lines[result_index]
        result_parts = result_line.split(':')
        result = result_parts[1].strip()

    expected = result == 'true'

    try:
        run_verification(test_case, jml.strip(), expected)
    except Exception as e:
        if not expected:
            LoggingHelper.log_error(e)
        else:
            LoggingHelper.log_info(e)


def run_verification(test_case: ConsistencyTestCase, jml: str, expected_result: bool):
    LoggingHelper.log_debug(f"Running verification with JML:\n {jml}", show_level=False)
    start_time = time.time()
    result = jml_verifier.verify(test_case, jml)
    end_time = time.time()
    if result.consistent is None:
        LoggingHelper.log_error(result)
    else:
        if result.consistent == expected_result:
            LoggingHelper.log_info(f"Verification successful in {end_time - start_time} seconds")
        else:
            LoggingHelper.log_error(f"Verification failed in {end_time - start_time} seconds")


def split(content, symbol):
    """
    Splits the content by the symbol.
    :param content: The content to split.
    :param symbol: The symbol to split by.
    :return: A list of the split content.
    """
    pattern_str = f'^{symbol}{{5,}}$'

    return re.split(pattern_str, content, flags=re.MULTILINE)


if __name__ == '__main__':
    jml_verifier = JmlVerifier()
    main()
