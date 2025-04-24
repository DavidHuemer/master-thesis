class BaseParameters:
    def parameter_exists(self, key: str) -> bool:
        """
        Check if a parameter exists in the parameters.
        :param key: The key of the parameter to check.
        :return: True if the parameter exists, False otherwise.
        """
        raise NotImplementedError

    def get_parameter_by_key(self, key: str, use_old: bool, use_this: bool):
        raise NotImplementedError
