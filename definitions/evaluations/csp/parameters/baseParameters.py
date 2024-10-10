class BaseParameters:
    def parameter_exists(self, key: str) -> bool:
        raise NotImplementedError

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        raise NotImplementedError
