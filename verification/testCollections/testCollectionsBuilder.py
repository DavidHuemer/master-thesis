from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.evaluations.tests.testCollections import TestCollections
from definitions.javaMethod import JavaMethod
from verification.testCollections.signalTestCollectionBuilder import SignalTestCollectionBuilder
from verification.testCollections.testCollectionBuilder import TestCollectionBuilder


class TestCollectionsBuilder:
    """
    Helper class for building TestCollections
    """

    def __init__(self, test_collection_builder=TestCollectionBuilder(),
                 signal_test_collection_builder=SignalTestCollectionBuilder()):
        self.test_collection_builder = test_collection_builder
        self.signal_test_collection_builder = signal_test_collection_builder

    def build(self, java_method: JavaMethod, ast: JmlTreeNode) -> TestCollections:
        """
        Build TestCollections from JavaMethod and AST
        :param java_method: The java method that should be tested for consistency
        :param ast: The AST of the JML annotations
        :return: The TestCollections
        """
        test_collection = self.test_collection_builder.build(java_method, ast.pre_conditions)

        # TODO: add signals test collection
        signal_collections = self.signal_test_collection_builder.build(java_method, ast.signals_conditions)

        return TestCollections(test_collection, signal_collections)
