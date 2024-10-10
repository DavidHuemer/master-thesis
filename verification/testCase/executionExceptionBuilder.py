from definitions.codeExecution.result.executionException import ExecutionException


class ExecutionExceptionBuilder:
    @staticmethod
    def build_exception(e) -> ExecutionException:
        if not hasattr(e, 'getClass'):
            raise Exception("Exception could not be built. The thrown exception does not have a class.")

        clazz = e.getClass()

        if not hasattr(clazz, 'getPackage'):
            raise Exception("Exception could not be built. The thrown exception class does not have a package.")

        package = str(clazz.getPackage().getName())

        if not hasattr(clazz, 'getSimpleName'):
            raise Exception("Exception could not be built. The thrown exception does not have a name.")

        name = str(clazz.getSimpleName())

        return ExecutionException(package_path=package, name=name)
