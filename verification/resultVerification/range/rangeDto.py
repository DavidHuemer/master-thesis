from definitions.evaluations.baseExecutinoDto import BaseExecutionDto
from definitions.evaluations.csp.parameters.rangeParameters import RangeParameters


class RangeDto(BaseExecutionDto):
    def __init__(self, node, range_parameters: RangeParameters, constraint_builder, result):
        super().__init__(node=node, parameters=range_parameters, result=result)
        self.node = node

        from verification.resultVerification.range.rangeBuilder import RangeBuilder
        self.constraint_builder: RangeBuilder = constraint_builder

    def copy_with_other_node(self, node):
        return RangeDto(node, self.get_range_parameters(), self.constraint_builder, self.result)

    def get_range_parameters(self) -> RangeParameters:
        if not isinstance(self.parameters, RangeParameters):
            raise Exception("RangeDto: Invalid parameters type")

        return self.parameters
