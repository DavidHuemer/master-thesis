class JmlTransformationExample:
    """
    Class that stores a JML transformation example
    """

    def __init__(self, java_doc: str, jml: str):
        self.java_doc = java_doc
        self.jml = jml

    def __eq__(self, other):
        return self.java_doc == other.java_doc and self.jml == other.jml

    def to_example(self) -> str:
        return f'JavaDoc:\n{self.java_doc}\nBecomes JML:\n{self.jml}'
