# movies/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import add_to_favorites,remove_from_favorites

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login , name='login'),
    path('category/<int:pk>/', views.category_filter, name='category'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('remove_favorite/<int:movie_id>/', views.remove_from_favorites, name='remove_from_favorites'),
   
    
]
