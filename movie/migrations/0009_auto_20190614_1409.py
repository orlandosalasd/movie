# Generated by Django 2.2.1 on 2019-06-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_auto_20190613_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]