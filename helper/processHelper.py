import subprocess


class ProcessHelper:
    """
    Helper class for process related operations
    """

    @staticmethod
    def check_with_commands(commands: list[str]):
        """
        Check the environment with commands
        :param commands: The commands to run
        :return: True if the commands ran successfully, False otherwise
        """

        try:
            ProcessHelper.check_output(commands)
        except subprocess.CalledProcessError:
            return False

        return True

    @staticmethod
    def check_output(commands: list[str]):
        """
        Run a command in the terminal
        :param commands: The commands to run
        :return: The output of the command
        """

        result = subprocess.check_output(
            commands,
            text=True, shell=False)
        return result

    @staticmethod
    def run_command(commands: list[str]):
        """
        Run a command in the terminal
        :param commands: The commands to run
        :return: The output of the command
        """

        result = subprocess.run(
            commands, check=True)
        return result
