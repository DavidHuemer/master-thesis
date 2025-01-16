from dependency_injector import containers, providers

from pipeline.jmlGenerator.JmlReceiver import JmlReceiver


class JmlIOContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    jml_receiver = providers.Factory(
        JmlReceiver
    )
