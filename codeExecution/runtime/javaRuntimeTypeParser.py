class JavaRuntimeTypeParser:
    @staticmethod
    def get_correct_type(java_type: str):
        if java_type == '[I':
            return 'int[]'
        elif java_type == '[D':
            return 'double[]'
        elif java_type == '[Ljava.lang.String;':
            return 'String[]'
        elif java_type == 'java.lang.String':
            return 'String'
        else:
            return java_type
