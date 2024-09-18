from definitions.code.classExtractionInfo import ClassExtractionInfo


class JavaCode:
    def __init__(self, file_path, class_info: ClassExtractionInfo, methods):
        self.file_path = file_path
        self.class_info = class_info
        self.methods = methods

    def __eq__(self, other):
        return (self.file_path == other.file_path
                and self.class_info == other.class_info
                and self.methods == other.methods)
