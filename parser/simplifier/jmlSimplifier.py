import parser.generated.JMLParser as JMLParser

from definitions.ast.behavior.behaviorNode import BehaviorNode
from definitions.ast.behavior.behaviorType import BehaviorType
from definitions.ast.exceptionExpression import ExceptionExpression
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.parserResult import ParserResult
from helper.objectHelper import ObjectHelper
from parser.simplificationDto import SimplificationDto
from parser.simplifier.allowedSignalsSimplifier import AllowedSignalsSimplifier
from parser.simplifier.rule_simplifier import RuleSimplifier


class JmlSimplifier:
    def __init__(self, rule_simplifier=RuleSimplifier(), allowed_signals_simplifier=AllowedSignalsSimplifier()):
        self.rule_simplifier = rule_simplifier
        self.allowed_signals_simplifier = allowed_signals_simplifier

        self.behavior_nodes: list[BehaviorNode] = []
        self.current_behavior: BehaviorNode = BehaviorNode()

    def simplify(self, jml: JMLParser.JMLParser.JmlContext, parser_result: ParserResult):
        """
        Simplifies the jml tree
        :param parser_result:
        :param jml:
        :return: The jml node containing all behavior nodes
        """

        jml_items = [jml_item for jml_item in jml.jml_item()]

        self.behavior_nodes = []
        self.current_behavior = BehaviorNode()
        self.behavior_nodes.append(self.current_behavior)

        for jml_item in jml_items:
            self.handle_jml_item(jml_item, parser_result)

        jml_node = JmlTreeNode(behavior_nodes=self.behavior_nodes)

        return jml_node

    def handle_jml_item(self, jml_item: JMLParser.JMLParser.Jml_itemContext, parser_result: ParserResult):
        if self.is_behavior_node(jml_item):
            self.handle_behavior_node(jml_item)
        else:
            self.handle_condition(jml_item, parser_result)

    def handle_condition(self, jml_item: JMLParser.JMLParser.Jml_itemContext, parser_result: ParserResult):
        condition = jml_item.cond.children[0]

        # Check if condition is @also -> create new behavior node
        if isinstance(condition, JMLParser.JMLParser.Also_conditionContext):
            self.current_behavior = BehaviorNode()
            self.behavior_nodes.append(self.current_behavior)
        else:
            self.handle_condition_expression(condition, parser_result)

    def handle_condition_expression(self, condition, parser_result: ParserResult):
        simplification_dto = SimplificationDto(condition.children[1], self.rule_simplifier, parser_result)

        if isinstance(condition, JMLParser.JMLParser.Signals_only_conditionContext):
            allowed_signals = self.allowed_signals_simplifier.simplify(condition)
            self.current_behavior.add_allowed_signals(allowed_signals)
            return

        expr = self.rule_simplifier.evaluate(simplification_dto)

        if isinstance(condition, JMLParser.JMLParser.Requires_conditionContext):
            self.current_behavior.add_pre_condition(expr)
        elif isinstance(condition, JMLParser.JMLParser.Ensures_conditionContext):
            self.current_behavior.add_post_condition(expr)
        elif isinstance(condition, JMLParser.JMLParser.Signals_conditionContext):
            if isinstance(expr, ExceptionExpression):
                self.current_behavior.add_signals_condition(expr)

    def handle_behavior_node(self, jml_item: JMLParser.JMLParser.Jml_itemContext):
        behavior_expr: JMLParser.JMLParser.Behavior_exprContext = jml_item.children[0]
        if self.current_behavior.defined:
            raise Exception("Behavior already defined")

        if isinstance(behavior_expr.children[1], JMLParser.JMLParser.Special_behaviorContext):
            special_behavior = behavior_expr.children[1]
            special_behavior_text = special_behavior.children[0].text

            if special_behavior_text == "normal_behavior":
                self.current_behavior.behavior_type = BehaviorType.NORMAL_BEHAVIOR
            elif special_behavior_text == "exceptional_behavior":
                self.current_behavior.behavior_type = BehaviorType.EXCEPTIONAL_BEHAVIOR

    @staticmethod
    def is_behavior_node(jml_item: JMLParser.JMLParser.Jml_itemContext):
        return ObjectHelper.check_has_child(jml_item, 'behavior')
