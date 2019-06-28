import os

from celery import chord, group

from moviespage.celery import app
# from celery._state import get_current_app
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from movie.models import Movie, Actor, Director, Suggest
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


@app.task()
def send_email(titles):
    # create message object instance
    msg = MIMEMultipart()

    message = 'The Movie/s '

    for title in titles:

        message = message + title + ', '

    message = message + ' was DOWNLOADED'

    # setup the parameters of the message
    password = "osd1143382275"
    msg['From'] = "orlandosalasdiaz1995@gmail.com"
    msg['To'] = "orlandosalasdiaz@hotmail.com"
    msg['Subject'] = "Movies"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    return print("successfully sent email to %s:" % (msg['To']))


@app.task()
def download_movie(title):

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
            if duration[0] != 'N/A':
                model.duration = int(duration[0])
            model.detail = response_two.json()['Plot']
            gender = response_two.json()['Genre']
            gender = gender.split(',')
            model.gender = gender[0]
            model.original_languaje = response_two.json()['Language']
            model.country = response_two.json()['Country']
            release_date = response_two.json()['Released']
            if release_date != 'N/A':
                model.release_date = datetime.strptime(release_date, '%d %b %Y')

            # Image
            image_url = response_two.json()['Poster']
            image_response = requests.get(image_url)
            image_response = image_response.content
            image = open(settings.MEDIA_ROOT + '/' + Title + '.jpg', 'wb')
            image.write(image_response)
            image.close()
            model.poster = Title + '.jpg'

            model.save()

            # Forey Key Actor
            Actors = response_two.json()['Actors']
            Actors = Actors.split(', ')
            tem_actor = []
            for actor in Actors:
                instance, get = Actor.objects.get_or_create(name=actor)
                tem_actor.append(instance)

            # Forey Key Director
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

    Suggest.objects.get(title=title).delete()

    return title


@app.task()
def valid_suggest():

    suggest_list = Suggest.objects.values_list('title', flat=True).distinct()

    if len(suggest_list) > 0:
        task_group = []
        for suggest in suggest_list:
            task_group.append(download_movie.s(suggest))
        chord(group(task_group), send_email.s()).delay()

    else:
        return print('no suggestions')
