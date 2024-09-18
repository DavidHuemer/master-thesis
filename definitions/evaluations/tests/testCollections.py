from definitions.evaluations.tests.testCollection import TestCollection


class TestCollections:
    def __init__(self, test_collection: TestCollection):
        self.test_collection = test_collection

    def __str__(self):
        return f"TestCollections: Nr of positive test cases: {len(self.test_collection.test_cases)}"
