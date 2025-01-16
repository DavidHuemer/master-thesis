from dependency_injector import containers, providers

from codeExecution.vm.VMHelper import VMHelper


class VmContainers(containers.DeclarativeContainer):
    vm = providers.Factory(
        VMHelper
    )
