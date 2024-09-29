class ObjectHelper:
    @staticmethod
    def check_has_child(obj, name: str):
        return hasattr(obj, name) and getattr(obj, name) is not None

    @staticmethod
    def check_child_text(obj, child_index: int, text: str):
        return (0 <= child_index < obj.getChildCount()
                and obj.children[child_index].getText() == text)
