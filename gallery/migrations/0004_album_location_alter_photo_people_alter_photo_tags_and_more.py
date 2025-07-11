# Generated by Django 5.0.14 on 2025-06-15 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0007_person_creator'),
        ('gallery', '0003_alter_photo_people_alter_photo_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Локация'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, related_name='photos', to='family_tree.person', verbose_name='Привязка к карточке'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='photos', to='gallery.tag', verbose_name='Привязка к тегам'),
        ),
        migrations.AlterField(
            model_name='video',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, related_name='videos', to='family_tree.person', verbose_name='Привязка к карточке'),
        ),
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='videos', to='gallery.tag', verbose_name='Привязка к тегам'),
        ),
    ]
