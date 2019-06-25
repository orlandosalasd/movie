from rest_framework import serializers

from movie.models import Movie, MovieRate


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    duration = serializers.IntegerField()
    gender = serializers.CharField(max_length=50)
    original_languaje = serializers.CharField(max_length=15)
    country = serializers.CharField(max_length=20)
    release_date = serializers.DateField()

    class Meta:
        model = Movie
        fields = ('title', 'duration', 'gender', 'original_languaje', 'country', 'release_date', 'poster')


class MovieRateSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieRate
        fields = ('rate', 'movie', 'user')






