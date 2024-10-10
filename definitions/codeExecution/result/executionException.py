class ExecutionException:
    def __init__(self, package_path: str, name: str):
        self.package_path = package_path
        self.name = name
        self.full_name = f"{package_path}.{name}"

    def __str__(self):
        return self.full_name
