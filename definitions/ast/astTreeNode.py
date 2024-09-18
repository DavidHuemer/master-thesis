class AstTreeNode:
    def __init__(self, name: str):
        self.name = name
        self.children: list[AstTreeNode] = []

    def get_tree_string(self):
        return self.name

    def to_string(self):
        return self.get_tree_string()

    def __str__(self):
        return self.get_tree_string()
