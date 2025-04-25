import threading
from collections.abc import Callable
from typing import Any

from definitions.timeoutException import TimeoutException


class TimeoutHelper:
    @staticmethod
    def run_with_timeout(method: Callable[[threading.Event], Any], timeout: float):
        # Funktion, die in einem Thread ausgeführt wird
        ergebnis = [None]
        stop_event = threading.Event()

        def wrapper():
            try:
                result = method(stop_event)
            except Exception as e:
                result = e

            ergebnis[0] = result

        # Thread starten
        thread = threading.Thread(target=wrapper)
        thread.start()

        # Auf den Thread warten, maximal 'zeit' Sekunden
        thread.join(timeout)

        if thread.is_alive():
            stop_event.set()
            raise TimeoutException(f"Die Methode hat die Zeit von {timeout} Sekunden überschritten!")

        if isinstance(ergebnis[0], Exception):
            raise ergebnis[0]

        return ergebnis[0]

    @staticmethod
    def timeout_handler(signum, frame):
        raise TimeoutException("Die Ausführung hat zu lange gedauert!")
