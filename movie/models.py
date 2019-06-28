from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from .choices import GENDERS, LENGUAJE

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Director(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


def movie_directory_path(instance, filename):
    return f'movie/{instance.title}/{filename}'


class Movie (models.Model):

    title = models.CharField(max_length=100)
    duration = models.IntegerField(null=True, blank=True)
    detail = models.TextField(max_length=500, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    original_languaje = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='actor', null=True, blank=True)
    directors = models.ManyToManyField(Director, related_name='director', null=True, blank=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.title}'


class MovieRate(models.Model):
    rate = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username} : {self.rate}'


class UserToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'


class Suggest(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'






