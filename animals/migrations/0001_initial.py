# Generated by Django 2.2.6 on 2019-11-21 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sexo', models.CharField(help_text='M --> Macho & H --> Hembra', max_length=5, verbose_name='Sexo')),
                ('raza', models.CharField(help_text='Ingrese la raza si lo considera necesario', max_length=100)),
                ('fecha_nac', models.DateField(help_text='Ingrese la fecha de nacimiento', verbose_name='Fecha de nacimiento')),
                ('edad', models.DateField(help_text='Se autocompleta a partir de la fecha indicada como nacimiento', verbose_name='Edad en dias')),
            ],
        ),
        migrations.CreateModel(
            name='Caravana',
            fields=[
                ('numero', models.IntegerField(primary_key=True, serialize=False)),
                ('CUIG', models.CharField(help_text='Buscar que es !!!!!!!', max_length=100)),
                ('RENSPA', models.CharField(help_text='Buscar que es !!!!!!!!!!!', max_length=100)),
                ('codRFID', models.IntegerField(help_text='Ingrese el codigo de RFID', unique=True, verbose_name='RFID')),
                ('color', models.CharField(help_text='Ingrese el color de la caravana', max_length=100, verbose_name='Color')),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(help_text='Ingrese el tipo de la vacuna', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalVacunado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Vacuna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animals.Vacuna')),
                ('animal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animals.Animal')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='caravana_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animals.Caravana'),
        ),
    ]