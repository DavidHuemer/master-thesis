from definitions.evaluations.BaseDto import BaseDto
from definitions.parser.parserResult import ParserResult
from nodes.baseNodeRunner import BaseNodeRunner


class SimplificationDto(BaseDto):
    def __init__(self, node, simplifier: BaseNodeRunner, parser_result: ParserResult):
        super().__init__(node, simplifier)
        self.parser_result = parser_result

    def copy_with_other_node(self, node):
        return SimplificationDto(node, self.runner, self.parser_result)
