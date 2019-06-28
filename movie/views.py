from uuid import uuid4

from celery import chord, group
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, RedirectView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListCreateAPIView, \
    RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from movie.forms import UserForm, MovieFormDownload
from movie.models import UserToken, Suggest
from movie.tasks import download_movie, send_email
from .choices import GENDERS
from .models import Movie
from .forms import MovieForm, AuthenticationForm
from api.serializers import MovieSerializer
from rest_framework.authtoken.models import Token


class MovieLogin(FormView):
    template_name = 'movie/index.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('movie:movie')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            username = request.POST['username']
            try:
                user = User.objects.get(username=username)
            except:
                user = None
            if user:
                password = form.cleaned_data.get("password")
                user_login = authenticate(username=username, password=password)
                request.session['user'] = user.username
                if user_login:
                    user_token = Token(user=user)
                    user_token.save()
                else:
                    return self.form_invalid(form)

            return self.form_valid(form)

        else:
            return self.form_invalid(form)


class MovieLogout(RedirectView):
    pattern_name = 'movie:index'

    def get(self, request, *args, **kwargs):

        try:
            username = request.session['user']
            user = User.objects.get(username=username)
            token = Token.objects.filter(user_id=user.id)
            token.delete()
            del request.session['user']
        except KeyError:
            pass
        return super(MovieLogout, self).get(request, *args, **kwargs)


class MovieListView(ListView):
    model = Movie
    template_name = 'movie/movie.html'

    def get_queryset(self):
        genre = self.request.GET.get('genre', None)
        qs = super(MovieListView, self).get_queryset()
        return qs.filter(gender=genre)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(MovieListView, self).get_context_data(object_list=object_list, **kwargs)
        dict_genders = dict(GENDERS)
        movie_categories = {movie: dict_genders.get(movie) for movie in
                            Movie.objects.values_list('gender', flat=True).distinct()}
        movie_list = Movie.objects.all()

        data.update({'categories': movie_categories, 'movie_list': movie_list})
        return data


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movie/moviecreator.html'
    success_url = 'movie/movie.html'


'''class MovieDownload(FormView):
    template_name = 'movie/download.html'
    success_url = reverse_lazy('movie:movie')
    form_class = MovieFormDownload

    def form_valid(self, form):
        titles = form.cleaned_data.get('title')
        titles = titles.split(', ')
        task_group = []
        for title in titles:
            task_group.append(download_movie.s(title))
        chord(group(task_group), send_email.s()).delay()

        return super().form_valid(form)'''


class MovieDownload(FormView):
    template_name = 'movie/download.html'
    success_url = reverse_lazy('movie:movie')
    form_class = MovieFormDownload

    def form_valid(self, form):
        titles = form.cleaned_data.get('title')
        titles = titles.split(', ')
        for title in titles:
            instance = Suggest.objects.create(title=title)
            instance.save()
        return super().form_valid(form)


# ---------------- API - SERIALIZERS -----------------------


class MovieList(BaseListView):
    model = Movie
    response_class = HttpResponse
    content_type = 'application/json'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieList, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data' : JSONRenderer().render(MovieSerializer(self.get_queryset(),many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class MovieDetail(BaseDetailView):
    model = Movie
    response_class = HttpResponse
    content_type = 'application/json'

    def get_context_data(self, *, object=None, **kwargs):
        context = super(MovieDetail, self).get_context_data(object=object, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieSerializer(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class MovieDetailXml(BaseDetailView):
    model = Movie
    response_class = HttpResponse
    content_type = 'application/xml'

    def get_context_data(self, *, object=None, **kwargs):
        context = super(MovieDetailXml, self).get_context_data(object=object, **kwargs)
        context.update({'serialized_data': XMLRenderer().render(MovieSerializer(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class MovieApiCreateList(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class MovieApiUpdateDelete(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    lookup_field = 'pk'

