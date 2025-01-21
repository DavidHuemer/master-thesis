from dependency_injector import containers, providers

from verification.resultVerification.executionVerifier import ExecutionVerifier


class ResultVerificationContainer(containers.DeclarativeContainer):
    execution_verifier = providers.Singleton(ExecutionVerifier)
