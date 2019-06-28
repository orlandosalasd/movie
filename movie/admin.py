from django.contrib import admin

from movie.models import Suggest
from .models import Actor, Director, Movie, MovieRate, UserToken

# Register your models here.

admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(MovieRate)
admin.site.register(UserToken)
admin.site.register(Suggest)

