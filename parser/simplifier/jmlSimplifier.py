import parser.generated.JMLParser as JMLParser
from definitions.ast.jmlTreeNode import JmlTreeNode
from definitions.parser.parserResult import ParserResult
from parser.simplifier.rule_simplifier import RuleSimplifier
from parser.simplifier.boolQuantifierSimplifier import BoolQuantifierSimplifier
from parser.tree.ruleMetaDataHelper import RuleMetaDataHelper


class JmlSimplifier:
    def __init__(self, rule_simplifier=RuleSimplifier(), meta_data_helper=RuleMetaDataHelper(),
                 bool_quantifier_simplifier=BoolQuantifierSimplifier()):
        self.rule_simplifier = rule_simplifier
        self.rule_meta_data_helper = meta_data_helper
        self.bool_quantifier_simplifier = bool_quantifier_simplifier

    def simplify(self, jml: JMLParser.JMLParser.JmlContext, parser_result: ParserResult):
        """
        Simplifies the jml tree
        :param parser_result:
        :param jml:
        :return:
        """

        jml_node = JmlTreeNode()
        conditions = [x.children[0] for x in jml.condition()]

        for condition in conditions:
            # Check if condition is a pre-condition (requires_conditionContext)
            if isinstance(condition, JMLParser.JMLParser.Requires_conditionContext):
                expr = self.rule_simplifier.simplify_rule(condition.children[2], parser_result)
                jml_node.add_pre_condition(expr)

            # TODO: Add support for signals condition (exception handling)

            # Check if condition is a post-condition (ensures_conditionContext)
            if isinstance(condition, JMLParser.JMLParser.Ensures_conditionContext):
                expr = self.rule_simplifier.simplify_rule(condition.children[2], parser_result)
                jml_node.add_post_condition(expr)

        return jml_node
