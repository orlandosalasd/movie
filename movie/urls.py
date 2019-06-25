from django.contrib.auth import login
from django.urls import path, include
from django.conf import settings

from movie.views import MovieList, MovieDetail, MovieDetailXml, MovieApiCreateList, MovieApiUpdateDelete, MovieLogin, \
    MovieLogout
from .views import MovieListView,MovieCreateView
from django.conf.urls.static import static

app_name = 'movie'

urlpatterns = [
    path('login/', MovieLogin.as_view(), name='index'),
    path('logout/', MovieLogout.as_view(), name='logout'),
    path('movie/', MovieListView.as_view(), name='movie'),
    path('moviecreator/', MovieCreateView.as_view()),
    path('api/', MovieList.as_view()),
    path('detail/<pk>',MovieDetail.as_view()),
    path('detailxml/<pk>',MovieDetailXml.as_view()),
    path('movieapi', MovieApiCreateList.as_view()),
    path('movieapi/<pk>', MovieApiUpdateDelete.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)