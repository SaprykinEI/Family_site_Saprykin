from django.core.cache import cache
from django.conf import settings
from family_tree.models import Person

import logging

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 60


def get_person_cache():
    """
    Получить список всех Person с кешированием.
    """
    if getattr(settings, 'CACHE_ENABLED', False):
        key = 'person_list'
        person_list = cache.get(key)
        if person_list is None:
            logger.info('Кеш пуст, загружаем из базы и кешируем')
            person_list = Person.objects.all()
            cache.set(key, person_list, CACHE_TIMEOUT)
        else:
            logger.info('Данные взяты из кеша')
    else:
        logger.info('Кеширование отключено, данные взяты из базы')
        person_list = Person.objects.all()

    return person_list


def get_descendants_tree_cached(person, build_tree_func):
    """
    Получить дерево потомков для person с кешированием.
    """
    cache_key = f'tree_data_{person.id}'
    data = cache.get(cache_key)

    if data is None:
        data = build_tree_func(person)
        cache.set(cache_key, data, CACHE_TIMEOUT)

    return data

def get_ancestors_tree_cached(person, build_tree_func):
    """
    Получить дерево предков для person с кешированием.
    """
    cache_key = f'spouse_tree_data_{person.id}'
    data = cache.get(cache_key)

    if data is None:
        data = build_tree_func(person)
        cache.set(cache_key, data, CACHE_TIMEOUT)

    return data



