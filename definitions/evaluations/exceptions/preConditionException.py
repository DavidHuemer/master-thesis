class PreConditionException(Exception):
    def __init__(self, message: str):
        super().__init__(f"Precondition not satisfied: {message}")
        self.message = message
