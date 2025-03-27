import os

from dotenv import load_dotenv

from definitions import envKeys
from definitions.envKeys import JML_FILE
from helper.logs.loggingHelper import log_info
from jml.jmlFileHelper import get_jml_file


def load_and_check_env_file(env_file: str):
    load_dotenv(f"env/{env_file}")
    check_environment()


def get_required_env_variables():
    return [item for item in dir(envKeys) if not item.startswith("__")]


def get_required_env_dict():
    env_dict = {key: value for key, value in os.environ.items() if key in get_required_env_variables()}
    env_dict[JML_FILE] = get_jml_file()
    return env_dict


def check_environment():
    """
    Checks whether all environment variables are set
    :return:
    """
    log_info("Checking environment variables")

    # Check if all variables are set
    for item in get_required_env_variables():
        if not os.getenv(item):
            raise Exception(f"Environment variable {item} is not set")
