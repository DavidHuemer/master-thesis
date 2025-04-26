from definitions.evaluations.BaseDto import BaseDto
from nodes.handlers.BaseArrayIndexNodeHandler import BaseArrayIndexNodeHandler


class BaseArrayIndexConstraintBuilder(BaseArrayIndexNodeHandler[BaseDto]):
    def __init__(self):
        super().__init__()
