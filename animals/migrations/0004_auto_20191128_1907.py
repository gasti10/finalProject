# Generated by Django 2.2.6 on 2019-11-28 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0003_auto_20191122_1844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ['-caravana_id'], 'verbose_name': 'Animal', 'verbose_name_plural': 'Animales'},
        ),
        migrations.AlterModelOptions(
            name='animalvacunado',
            options={'ordering': ['-animal'], 'verbose_name': 'Animal vacunado', 'verbose_name_plural': 'Animales vacunados'},
        ),
        migrations.AlterModelOptions(
            name='caravana',
            options={'ordering': ['-numero'], 'verbose_name': 'Caravana', 'verbose_name_plural': 'Caravanas'},
        ),
        migrations.AlterModelOptions(
            name='vacuna',
            options={'ordering': ['-id'], 'verbose_name': 'Vacuna', 'verbose_name_plural': 'Vacunas'},
        ),
        migrations.RenameField(
            model_name='animalvacunado',
            old_name='Vacuna',
            new_name='vacuna',
        ),
    ]
