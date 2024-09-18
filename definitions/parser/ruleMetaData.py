class RuleMetaData:
    def __init__(self, name: str, rule_parts: list[str]):
        self.name = name
        self.rule_parts = rule_parts

    def can_simplify(self) -> bool:
        # Return true when the rule_parts have a "simplify" element
        return "simplify" in self.rule_parts

    def include_terminal_children(self) -> bool:
        # Return true when the rule_parts have an "include_terminal_children" element
        return "include_terminal_children" in self.rule_parts

    def __str__(self) -> str:
        return (f"RuleMetaData(name={self.name}, "
                f"can_simplify={self.can_simplify()}, "
                f"include_terminal_children={self.include_terminal_children()})")
