# Generated by Django 2.2.1 on 2019-06-07 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('duration', models.TimeField()),
                ('detail', models.TextField(max_length=500)),
                ('gender', models.CharField(choices=[('drama', 'Drama'), ('science fiction', 'Science fiction'), ('action', 'Action'), ('terror', 'Terror'), ('adventures', 'Adventures'), ('intrigue', 'Intrigue'), ('romance', 'Romance'), ('animation', 'Animation'), ('suspense', 'Suspense'), ('musical', 'Musical')], max_length=50)),
                ('original_languaje', models.CharField(choices=[('english', 'English'), ('spanish', 'Spanish'), ('french', 'French'), ('german', 'German'), ('italian', 'Italian'), ('portuguese', 'Portuguese'), ('russian', 'Russian'), ('turkish', 'Turkish'), ('dutch', 'Dutch'), ('swedish', 'Swedish'), ('polish', 'Polish'), ('norwegian', 'Norwegian'), ('indonesian', 'Indonesian')], max_length=15)),
                ('country', models.CharField(max_length=20)),
                ('release_date', models.DateField()),
                ('poster', models.ImageField(upload_to='')),
                ('trailer_url', models.URLField()),
                ('actors', models.ManyToManyField(to='movie.Actor')),
                ('directors', models.ManyToManyField(to='movie.Director')),
            ],
        ),
    ]
