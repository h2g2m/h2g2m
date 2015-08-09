from h2g2m.lib.dependencyinjection import Container
from h2g2m.lib.repositories import LanguageRepository
from pyramid.path import AssetResolver


def init_container(container):
    """
    @type container: Container
    """
    container.provide('language_resource', lambda: AssetResolver('h2g2m').resolve('resources/en.json').abspath())

    container.provide('language_repository', lambda: LanguageRepository(container['language_resource']))

    return container