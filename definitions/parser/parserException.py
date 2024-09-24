class ParserException(Exception):
    def __init__(self, message, error_node=None):
        super().__init__(message)
        self.error_node = error_node
