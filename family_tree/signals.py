from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from family_tree.models import Person

CACHE_TIMEOUT = 60 * 60


def clear_person_cache(person_id):
    """Удаляет кеш для конкретного человека."""
    keys = [
        f'tree_data_{person_id}',
        f'ancestors_tree_data_{person_id}',
    ]
    for key in keys:
        cache.delete(key)


@receiver(post_save, sender=Person)
def on_person_save(sender, instance, **kwargs):
    """
        Обработчик сигнала post_save для модели Person.
        При сохранении человека:
        - Очищает кеш его дерева (потомков/предков).
        - Очищает кеши родителей и супруга.
        - Удаляет кеш списка всех людей.
    """
    print(f"Person saved: {instance.id}")
    clear_person_cache(instance.id)

    if instance.father_id:
        clear_person_cache(instance.father_id)
    if instance.mother_id:
        clear_person_cache(instance.mother_id)
    if instance.spouse_id:
        clear_person_cache(instance.spouse_id)

    # Очищаем кеш списка всех людей
    cache.delete('person_list')


@receiver(post_delete, sender=Person)
def on_person_delete(sender, instance, **kwargs):
    """
        Обработчик сигнала post_delete для модели Person.
        При удалении человека:
        - Очищает его кешированные данные (дерево предков/потомков).
        - Удаляет кеш общего списка людей.
    """
    clear_person_cache(instance.id)
    cache.delete('person_list')
