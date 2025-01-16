from dependency_injector import containers, providers

from parser.simplifier.jmlSimplifier import JmlSimplifier


class ParserContainer(containers.DeclarativeContainer):
    simplifier = providers.Singleton(JmlSimplifier)
