from definitions.parser.ruleMetaData import RuleMetaData
from helper.files.fileReader import FileReader


class RuleMetaDataLoader:
    def __init__(self, file_reader=FileReader):
        self.file_reader = file_reader

    def load_rule_meta_data(self):
        rules_meta_content = self.file_reader.read("data/parser/rule_meta.txt")
        rules_meta_lines = rules_meta_content.split("\n")

        # Filter out empty lines
        rules_meta_lines = list(filter(lambda s: s != '', rules_meta_lines))
        rules_dict = {}

        for line in rules_meta_lines:
            rule_parts = line.split(";")
            if len(rule_parts) <= 0:
                continue

            rule_name = rule_parts[0]
            rules_dict[rule_name] = RuleMetaData(rule_name, rule_parts[1:])

        return rules_dict
