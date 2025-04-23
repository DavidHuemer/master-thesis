consistency_logs: list[str] = []


def clear_consistency_logs():
    """
    Clear the consistency logs.
    """
    global consistency_logs
    consistency_logs = []


def add_consistency_log(log: str):
    """
    Add a log to the consistency logs.
    :param log: The log to add.
    """
    global consistency_logs
    consistency_logs.append(log)


def get_consistency_logs():
    # return a copy of the global consistency_logs
    global consistency_logs
    return consistency_logs.copy()
