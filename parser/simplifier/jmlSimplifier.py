import parser.generated.JMLParser as JMLParser

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.parserResult import ParserResult
from parser.simplificationDto import SimplificationDto
from parser.simplifier.allowedSignalsSimplifier import AllowedSignalsSimplifier
from parser.simplifier.rule_simplifier import RuleSimplifier
from util.Singleton import Singleton


class JmlSimplifier(Singleton):
    def __init__(self, rule_simplifier=None, allowed_signals_simplifier=None):
        self.rule_simplifier = rule_simplifier or RuleSimplifier()
        self.allowed_signals_simplifier = allowed_signals_simplifier or AllowedSignalsSimplifier()

        self.behavior_nodes: list[BehaviorNode] = []

    def simplify(self, jml: JMLParser.JMLParser.JmlContext, parser_result: ParserResult):
        """
        Simplifies the jml tree
        :param parser_result:
        :param jml:
        :return: The jml node containing all behavior nodes
        """

        jml_contract: JMLParser.JMLParser.ContractContext = jml.contract()
        behavior_nodes: list[BehaviorNode] = []
        for behavior_expr in jml_contract.children:
            if isinstance(behavior_expr, JMLParser.JMLParser.Behavior_exprContext):
                behavior = behavior_expr.children[0]
                behavior_nodes.append(self.get_behavior_node(behavior, parser_result))

        return JmlTreeNode(behavior_nodes=behavior_nodes)

    def get_behavior_node(self, behavior, parser_result):
        behavior_node = BehaviorNode()
        behavior_node.behavior_type = self.get_behavior_type(behavior)
        self.handle_behavior(behavior_node, behavior, parser_result)
        return behavior_node

    @staticmethod
    def get_behavior_type(behavior):
        if isinstance(behavior, JMLParser.JMLParser.Default_behaviorContext):
            return BehaviorType.DEFAULT
        elif isinstance(behavior, JMLParser.JMLParser.Normal_behaviorContext):
            return BehaviorType.NORMAL_BEHAVIOR
        elif isinstance(behavior, JMLParser.JMLParser.Exceptional_behaviorContext):
            return BehaviorType.EXCEPTIONAL_BEHAVIOR
        else:
            raise Exception("Unknown behavior type")

    def handle_behavior(self, behavior_node, behavior, parser_result: ParserResult):
        for condition in behavior.children:
            if isinstance(condition, JMLParser.JMLParser.ConditionContext):
                self.handle_condition_expression(behavior_node, condition.children[0], parser_result)

    def handle_condition_expression(self, behavior_node, condition, parser_result: ParserResult):
        if isinstance(condition, JMLParser.JMLParser.Signals_only_conditionContext):
            allowed_signals = self.allowed_signals_simplifier.simplify(condition)
            behavior_node.add_allowed_signals(allowed_signals)
            return
        simplification_dto = SimplificationDto(condition.children[1], parser_result)
        expr = self.rule_simplifier.evaluate(simplification_dto)

        if isinstance(condition, JMLParser.JMLParser.Requires_conditionContext):
            behavior_node.add_pre_condition(expr)
        elif isinstance(condition, JMLParser.JMLParser.Ensures_conditionContext):
            behavior_node.add_post_condition(expr)
        elif isinstance(condition, JMLParser.JMLParser.Signals_conditionContext):
            if isinstance(expr, ExceptionExpression):
                behavior_node.add_signals_condition(expr)
