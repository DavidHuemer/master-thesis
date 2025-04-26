from definitions.evaluations.BaseDto import BaseDto
from nodes.handlers.BasePrefixHandler import BasePrefixHandler


class BasePrefixConstraintBuilder(BasePrefixHandler[BaseDto]):
    def __init__(self):
        super().__init__(True)
