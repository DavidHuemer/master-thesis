from dependency_injector import containers, providers

from pipeline.consistencyResultGetter import ConsistencyResultGetter


class PipelineContainer(containers.DeclarativeContainer):
    jml_provider = providers.Dependency()

    consistency_result_getter = providers.Factory(
        ConsistencyResultGetter,
        jml_provider=jml_provider
    )
