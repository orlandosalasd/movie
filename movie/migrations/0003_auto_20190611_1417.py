# Generated by Django 2.2.1 on 2019-06-11 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20190610_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.IntegerField(),
        ),
    ]
