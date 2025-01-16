from nodes.baseNodeHandler import BaseNodeHandler
from testGeneration.constraints.boolQuantifierConstraintBuilder import BoolQuantifierConstraintBuilder
from testGeneration.constraints.constraintsDto import ConstraintsDto
from testGeneration.constraints.quantifier.numQuantifierConstraintBuilder import NumQuantifierConstraintBuilder


class QuantifierConstraintBuilder(BaseNodeHandler[ConstraintsDto]):
    def __init__(self, bool_quantifier_constraint_builder=BoolQuantifierConstraintBuilder(),
                 num_quantifier_constraint_builder=NumQuantifierConstraintBuilder()):
        self.bool_quantifier_constraint_builder = bool_quantifier_constraint_builder
        self.num_quantifier_constraint_builder = num_quantifier_constraint_builder

    def is_node(self, t: ConstraintsDto):
        return self.bool_quantifier_constraint_builder.is_node(t) or self.num_quantifier_constraint_builder.is_node(t)

    def handle(self, t: ConstraintsDto):
        if self.bool_quantifier_constraint_builder.is_node(t):
            return self.bool_quantifier_constraint_builder.handle(t)
        elif self.num_quantifier_constraint_builder.is_node(t):
            return self.num_quantifier_constraint_builder.handle(t)

        raise Exception("QuantifierConstraintBuilder: Invalid node")
