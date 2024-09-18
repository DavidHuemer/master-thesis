from definitions.parser.ruleMetaData import RuleMetaData
from parser.generated.JMLParser import JMLParser
from parser.tree.ruleMetaDataLoader import RuleMetaDataLoader


class RuleMetaDataHelper:
    def __init__(self, loader=RuleMetaDataLoader()):
        self.loader = loader
        self.rule_meta: dict[str, RuleMetaData] | None = None

    def get_meta_data_for_rule(self, rule, parser: JMLParser) -> RuleMetaData:
        if self.rule_meta is None:
            self.rule_meta = self.loader.load_rule_meta_data()

        name = self.get_name_of_rule(rule, parser)
        if name in self.rule_meta:
            return self.rule_meta[name]

        return RuleMetaData(name, [])

    def get_name_of_rule(self, rule, parser: JMLParser):
        return parser.ruleNames[rule.getRuleIndex()]
