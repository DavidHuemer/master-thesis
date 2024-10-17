import threading
from collections.abc import Callable
from typing import Any

from definitions.timeoutException import TimeoutException


class TimeoutHelper:
    @staticmethod
    def run_with_timeout(method: Callable[[threading.Event], Any], timeout: int):
        # Funktion, die in einem Thread ausgeführt wird
        ergebnis = [None]
        stop_event = threading.Event()

        def wrapper():
            ergebnis[0] = method(stop_event)

        # Thread starten
        thread = threading.Thread(target=wrapper)
        thread.start()

        # Auf den Thread warten, maximal 'zeit' Sekunden
        thread.join(timeout)

        if thread.is_alive():
            stop_event.set()
            raise TimeoutException(f"Die Methode hat die Zeit von {timeout} Sekunden überschritten!")

        return ergebnis[0]

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutException("Die Ausführung hat zu lange gedauert!")
