from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet
from.views import (MovieListView,MovieDetailView)
router=DefaultRouter()
router.register('movie/',MovieViewSet, basename='movie' )


urlpatterns=[
    path('profiles/',MovieListView.as_view(),name='movie_list'),
    path('<int:pk>/',MovieDetailView.as_view(),name='movie_detail'),

]+router.urls