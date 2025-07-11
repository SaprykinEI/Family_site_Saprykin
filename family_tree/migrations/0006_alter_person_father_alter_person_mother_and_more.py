# Generated by Django 5.0.14 on 2025-05-22 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_tree', '0005_alter_person_options_person_father_person_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_from_father', to='family_tree.person', verbose_name='Отец'),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_from_mother', to='family_tree.person', verbose_name='Мать'),
        ),
        migrations.AlterField(
            model_name='person',
            name='spouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spouses', to='family_tree.person', verbose_name='Супруг(а)'),
        ),
    ]
