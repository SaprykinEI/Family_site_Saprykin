# Generated by Django 5.0.14 on 2025-05-21 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0002_person_maiden_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата Смерти'),
        ),
        migrations.AlterField(
            model_name='person',
            name='favorite_food',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Любимая еда'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='person',
            name='hobbies',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Хобби'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='person',
            name='maiden_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Девичья фамилия'),
        ),
        migrations.AlterField(
            model_name='person',
            name='patronymic',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='person',
            name='playlist',
            field=models.URLField(blank=True, null=True, verbose_name='Любимая музыка'),
        ),
        migrations.AlterField(
            model_name='person',
            name='profession',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Профессия'),
        ),
    ]
