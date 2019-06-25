from django.urls import path
from api.viewsets import MovieViewSet


urlpatterns = [
path('movieapi', MovieViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('movieapi/<pk>', MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]