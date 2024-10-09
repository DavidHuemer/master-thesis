from definitions.parser.parserResult import ParserResult


class SimplifierDto:
    def __init__(self, rule, rule_simplifier, parser_result: ParserResult):
        from parser.simplifier.rule_simplifier import RuleSimplifier

        self.rule = rule
        self.rule_simplifier: RuleSimplifier = rule_simplifier
        self.parser_result = parser_result
