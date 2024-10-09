class CspFunctionNameGenerator:
    def get_name(self, names: list[str], required_name: str = 'f'):
        # Check if required_name is already in use (require_name is in functions list)
        if required_name not in names:
            return required_name
        else:
            return self.get_name_with_index(names, required_name, 0)

    def get_name_with_index(self, names: list[str], required_name: str, index: int):
        new_name = f"{required_name}_{index}"
        if new_name not in names:
            return new_name
        else:
            return self.get_name_with_index(names, required_name, index + 1)
