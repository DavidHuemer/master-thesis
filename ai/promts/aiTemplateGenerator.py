class AiTemplateGenerator:
    @staticmethod
    def generate_by_exception(exception_text: str):
        return (f"The following exception occurred:\n"
                f"{exception_text}\n"
                "Please provide a new JML for the method.\n"
                "Again, only generate the JML and nothing else, as the result is being parsed.")
