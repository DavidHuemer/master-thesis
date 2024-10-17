import threading
from collections.abc import Callable
from typing import Any

from definitions.timeoutException import TimeoutException


class TimeoutHelper:
    @staticmethod
    def run_with_timeout(method: Callable[[], Any], timeout: int):
        # Funktion, die in einem Thread ausgeführt wird
        ergebnis = [None]

        def wrapper():
            ergebnis[0] = method()

        # Thread starten
        thread = threading.Thread(target=wrapper)
        thread.start()

        # Auf den Thread warten, maximal 'zeit' Sekunden
        thread.join(timeout)

        if thread.is_alive():
            raise TimeoutException(f"Die Methode hat die Zeit von {timeout} Sekunden überschritten!")

        return ergebnis[0]

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutException("Die Ausführung hat zu lange gedauert!")
