from definitions.consistencyTestCase import ConsistencyTestCase
from helper.files.jsonFileHelper import JsonFileHelper


def get_stored_jml_for_test_case(path: str, test_case: ConsistencyTestCase) -> str:
    return get_jml_for_method(path, test_case.get_name())


def get_jml_for_method(path: str, method_name: str) -> str | None:
    jml_items = get_jml(path)

    if method_name in jml_items:
        return jml_items[method_name]

    return None


def get_jml(path: str) -> dict:
    return JsonFileHelper.read_json_file(path)


def store_jml_for_test_case(path: str, test_case: ConsistencyTestCase, jml: str):
    store_jml(path, test_case.get_name(), jml)


def store_jml(path: str, method_name: str, jml: str):
    jml_items = get_jml(path)

    jml_items[method_name] = jml

    JsonFileHelper.write_json_file(path, jml_items)
