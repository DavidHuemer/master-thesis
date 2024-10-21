from unittest import TestCase

from definitions.timeoutException import TimeoutException
from helper.timeout.timeoutHelper import TimeoutHelper


class TestTimeoutHelper(TestCase):
    def setUp(self):
        self.timeout_helper = TimeoutHelper()

    def test_run_with_timeout(self):
        # Check that the method raises a TimeoutException
        with self.assertRaises(TimeoutException):
            self.timeout_helper.run_with_timeout(method=lambda stop_event: self.sleep_example(1), timeout=.5)

    def test_get_result_works(self):
        # Check that the method returns the expected result
        self.timeout_helper.run_with_timeout(method=lambda stop_event: self.sleep_example(.1), timeout=.5)

    @staticmethod
    def sleep_example(time_sleep: float):
        import time
        time.sleep(time_sleep)
        return 1
