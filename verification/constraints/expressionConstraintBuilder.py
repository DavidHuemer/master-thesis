from z3 import If

from definitions.ast.arrayIndexNode import ArrayIndexNode
from definitions.ast.arrayLengthNode import ArrayLengthNode
from definitions.ast.astTreeNode import AstTreeNode
from definitions.ast.infixExpression import InfixExpression
from definitions.ast.methodCallNode import MethodCallNode
from definitions.ast.prefixNode import PrefixNode
from definitions.ast.quantifier.boolQuantifierTreeNode import BoolQuantifierTreeNode
from definitions.ast.quantifier.numQuantifierTreeNode import NumQuantifierTreeNode
from definitions.ast.questionMarkNode import QuestionMarkNode
from definitions.ast.terminalNode import TerminalNode
from definitions.evaluations.csp.jmlProblem import JMLProblem
from definitions.evaluations.csp.parameters.cspParamHelperType import CSPParamHelperType
from definitions.evaluations.csp.parameters.jmlParameters import JmlParameters
from helper.infixHelper import InfixHelper
from verification.constraints.boolQuantifierConstraintBuilder import BoolQuantifierConstraintBuilder
from verification.constraints.prefixConstraintBuilder import PrefixConstraintBuilder
from verification.constraints.quantifier.numQuantifierConstraintBuilder import NumQuantifierConstraintBuilder
from verification.constraints.terminalConstraintBuilder import TerminalConstraintBuilder


class ExpressionConstraintBuilder:
    def __init__(self, terminal_constraint_builder=TerminalConstraintBuilder(),
                 bool_quantifier_constraint_builder=BoolQuantifierConstraintBuilder(),
                 num_quantifier_constraint_builder=NumQuantifierConstraintBuilder(),
                 infix_helper=InfixHelper(), prefix_constraint_builder=PrefixConstraintBuilder()):
        self.terminal_constraint_builder = terminal_constraint_builder
        self.bool_quantifier_constraint_builder = bool_quantifier_constraint_builder
        self.infix_helper = infix_helper
        self.num_quantifier_constraint_builder = num_quantifier_constraint_builder
        self.prefix_constraint_builder = prefix_constraint_builder

    def build_expression_constraint(self, jml_problem: JMLProblem, jml_parameters: JmlParameters,
                                    expression: AstTreeNode):
        if isinstance(expression, TerminalNode):
            return self.terminal_constraint_builder.evaluate_terminal_node(expression, jml_parameters)

        if isinstance(expression, BoolQuantifierTreeNode):
            return self.bool_quantifier_constraint_builder.evaluate(jml_problem, jml_parameters, expression, self)

        if isinstance(expression, NumQuantifierTreeNode):
            return self.num_quantifier_constraint_builder.evaluate(jml_problem, jml_parameters, expression, self)

        if isinstance(expression, InfixExpression) and hasattr(expression, "left") and hasattr(expression, "right"):
            return self.infix_helper.evaluate_infix(infix_operator=expression.name,
                                                    left=lambda: self.build_expression_constraint(jml_problem,
                                                                                                  jml_parameters,
                                                                                                  expression.left),
                                                    right=lambda: self.build_expression_constraint(jml_problem,
                                                                                                   jml_parameters,
                                                                                                   expression.right),
                                                    is_smt=True, parameters=jml_parameters)

        if isinstance(expression, QuestionMarkNode):
            return If(self.build_expression_constraint(jml_problem, jml_parameters, expression.expr),
                      self.build_expression_constraint(jml_problem, jml_parameters, expression.true_expr),
                      self.build_expression_constraint(jml_problem, jml_parameters, expression.false_expr))

        if isinstance(expression, ArrayIndexNode):
            array = self.build_expression_constraint(jml_problem, jml_parameters, expression.arr_expression)
            expr = self.build_expression_constraint(jml_problem, jml_parameters, expression.index_expression)
            return array[expr]

        if isinstance(expression, ArrayLengthNode):
            arr_name = expression.arr_expr
            if hasattr(arr_name, 'value'):
                return jml_parameters.csp_parameters.get_helper(arr_name.value, CSPParamHelperType.LENGTH).value
            else:
                raise Exception("Array length expression not supported")

        if isinstance(expression, PrefixNode):
            return self.prefix_constraint_builder.evaluate(expression, jml_problem, jml_parameters, self)

        if isinstance(expression, MethodCallNode):
            raise Exception("Method call expression not supported")

        raise Exception("ExpressionConstraintBuilder: Expression type not supported")
