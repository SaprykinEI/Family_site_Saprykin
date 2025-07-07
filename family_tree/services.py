from django.core.cache import cache
from django.conf import settings
from family_tree.models import Person

import logging

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 60


def get_person_cache():
    """
    Возвращает список всех объектов Person, отсортированных по фамилии и имени.
    Использует кеширование, если оно включено в настройках.
    - Если данные есть в кеше — возвращает их оттуда.
    - Если нет — загружает из базы, кладёт в кеш и возвращает.
    """
    if getattr(settings, 'CACHE_ENABLED', False):
        key = 'person_list'
        person_list = cache.get(key)
        if person_list is None:
            logger.info('Кеш пуст, загружаем из базы и кешируем')
            person_list = Person.objects.all().order_by('last_name', 'first_name')
            cache.set(key, person_list, CACHE_TIMEOUT)
        else:
            logger.info('Данные взяты из кеша')
    else:
        logger.info('Кеширование отключено, данные взяты из базы')
        person_list = Person.objects.all().order_by('last_name', 'first_name')

    return person_list


def get_descendants_tree_cached(person, build_tree_func):
    """
    Получить дерево потомков для person с кешированием.
    Если дерево уже сохранено в кеше — взять его оттуда.
    Если нет — построить с помощью переданной функции и сохранить в кеше.
    Параметры:
        person (Person): Человек, для которого строим дерево.
        build_tree_func (callable): Функция, которая возвращает дерево потомков для данного человека.
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
    Если данные уже есть в кеше — взять их оттуда.
    Если нет — построить дерево с помощью переданной функции и сохранить в кеш.
    Параметры:
        person (Person): Человек, для которого строим дерево предков.
        build_tree_func (callable): Функция, которая возвращает дерево предков для данного человека.
    """
    cache_key = f'ancestors_tree_data_{person.id}'
    data = cache.get(cache_key)

    if data is None:
        data = build_tree_func(person)
        cache.set(cache_key, data, CACHE_TIMEOUT)

    return data



