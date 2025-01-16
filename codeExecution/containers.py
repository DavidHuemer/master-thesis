from dependency_injector import containers, providers

from codeExecution.vm.containers import VmContainers


class CodeExecutionContainers(containers.DeclarativeContainer):
    vm = providers.Container(
        VmContainers
    )
