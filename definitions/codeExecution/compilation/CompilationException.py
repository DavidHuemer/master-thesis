class CompilationException(BaseException):
    def __init__(self, message):
        super().__init__(f'Compilation failed: {message}')
