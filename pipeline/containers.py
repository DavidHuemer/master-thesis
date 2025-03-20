from dependency_injector import containers, providers

from pipeline.consistencyResultGetter import ConsistencyResultRunner


class PipelineContainer(containers.DeclarativeContainer):
    jml_provider = providers.Dependency()

    consistency_result_getter = providers.ThreadSafeSingleton(
        ConsistencyResultRunner,
        jml_provider=jml_provider
    )
