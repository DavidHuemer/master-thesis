from definitions.evaluations.tests.signalTestCollection import SignalTestCollection
from definitions.evaluations.tests.testCollection import TestCollection


class TestCollections:
    def __init__(self, test_collection: TestCollection, signal_collections: list[SignalTestCollection]):
        self.test_collection = test_collection
        self.signal_collections = signal_collections

    def __str__(self):
        return f"TestCollections: Nr of positive test cases: {len(self.test_collection.test_cases)}"

    def get_test_cases_count(self):
        return (self.test_collection.get_test_cases_count()
                + sum([
                    signal_collection.get_test_cases_count() for signal_collection in self.signal_collections
                ]))
