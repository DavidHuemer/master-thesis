from nodes.baseNodeHandler import BaseNodeHandler
from parser.simplifier.quantifier_simplifier.boolQuantifierSimplifier import BoolQuantifierSimplifier
from parser.simplifier.quantifier_simplifier.numericQuantifierSimplifier import NumericQuantifierSimplifier
from parser.simplifier.simplifierDto import SimplifierDto
import parser.generated.JMLParser as JMLParser


class QuantifierSimplifier(BaseNodeHandler[SimplifierDto]):
    def __init__(self, bool_quantifier_simplifier=BoolQuantifierSimplifier(),
                 numeric_quantifier_simplifier=NumericQuantifierSimplifier()):
        super().__init__()
        self.bool_quantifier_simplifier = bool_quantifier_simplifier
        self.numeric_quantifier_simplifier = numeric_quantifier_simplifier

    def is_node(self, t: SimplifierDto):
        return isinstance(t.rule, JMLParser.JMLParser.Quantifier_expressionContext)

    def handle(self, t: SimplifierDto):
        if self.bool_quantifier_simplifier.is_node(t):
            return self.bool_quantifier_simplifier.handle(t)
        elif self.numeric_quantifier_simplifier.is_node(t):
            return self.numeric_quantifier_simplifier.handle(t)

        raise Exception("QuantifierSimplifier: Rule is not a quantified expression")
