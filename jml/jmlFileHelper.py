import os
import time

from definitions.envKeys import JML_FILE


def get_jml_file():
    if os.getenv(JML_FILE) and os.path.exists(os.getenv(JML_FILE)):
        return os.getenv(JML_FILE)

    # combine jml-results with the current timestamp
    return os.path.join("jml-results", f"jml-{int(time.time())}.json")
