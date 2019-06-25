import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from movie.models import Movie, Actor, Director
from datetime import datetime



class Command(BaseCommand):
    help = 'fetch movie from OMDB API'

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)

    def handle(self, *args, **options):
        search = options['search']
        title = options['title']
        print(search)
        print(title)
        if search:
            url = 'http://www.omdbapi.com/?{}={}&plot=full&apikey=4ae80ea6'.format('s', title)
            response = requests.get(url)
            for i in response.json()['Search']:
                if not Movie.objects.filter(title=i['Title']).exists():
                    key = i['imdbID']
                    response_two = requests.get('http://www.omdbapi.com/?i={}&plot=full&apikey=4ae80ea6'.format(key))
                    model = Movie()
                    Title = response_two.json()['Title']
                    model.title = response_two.json()['Title']
                    duration = response_two.json()['Runtime']
                    duration = duration.split()
                    model.duration = duration[0]
                    model.detail = response_two.json()['Plot']
                    gender = response_two.json()['Genre']
                    gender = gender.split(',')
                    model.gender = gender[0]
                    model.original_languaje = response_two.json()['Language']
                    model.country = response_two.json()['Country']
                    release_date = response_two.json()['Released']
                    model.release_date = datetime.strptime(release_date, '%d %b %Y')

                    #Image
                    image_url = response_two.json()['Poster']
                    image_response = requests.get(image_url)
                    image_response = image_response.content
                    image = open(settings.MEDIA_ROOT + '/' + Title + '.jpg', 'wb')
                    image.write(image_response)
                    image.close()
                    model.poster = Title + '.jpg'

                    model.save()

                    #Forey Key Actor
                    Actors = response_two.json()['Actors']
                    Actors = Actors.split(', ')
                    tem_actor = []
                    for actor in Actors:
                        instance, get = Actor.objects.get_or_create(name=actor)
                        tem_actor.append(instance)



                    #Forey Key Director
                    Directors = response_two.json()['Director']
                    Directors = Directors.split(', ')
                    tem_director = []
                    for director in Directors:
                        instance, get = Director.objects.get_or_create(name=director)
                        tem_director.append(instance)

                    model = Movie.objects.get(title=Title)
                    for j in tem_actor:
                        model.actors.add(j)

                    for k in tem_director:
                        model.directors.add(k)

                    model.save()




