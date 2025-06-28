from django.db import migrations, models
from django.utils.text import slugify

def fill_slugs(apps, schema_editor):
    Person = apps.get_model('family_tree', 'Person')
    existing_slugs = set()

    for person in Person.objects.all():
        base_slug = slugify(f"{person.first_name} {person.last_name}") or "person"
        slug = base_slug
        suffix = 1
        while slug in existing_slugs or Person.objects.filter(slug=slug).exclude(pk=person.pk).exists():
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        person.slug = slug
        person.save()
        existing_slugs.add(slug)

class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0007_person_creator'),  # замени на свою последнюю миграцию
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, null=True),
        ),
        migrations.RunPython(fill_slugs),
        migrations.AlterField(
            model_name='person',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
