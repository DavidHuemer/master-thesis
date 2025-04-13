class JavaRuntimeTypeParser:
    @staticmethod
    def get_correct_type(java_type: str):
        if java_type == '[I':
            return 'int[]'
        elif java_type == '[D':
            return 'double[]'
        elif java_type == '[Ljava.lang.String;':
            return 'String[]'

        # Check if the type contains 'java.lang.' and remove it
        if 'java.lang.' in java_type:
            return java_type.replace('java.lang.', '')

        return java_type
