# movies/admin.py
from django.contrib import admin
from .models import Genre, Director, Actor, Movie, Comment,Category


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration', 'director')
    search_fields = ('title',)
    list_filter = ('genres','categories','release_date')
    filter_horizontal = ('genres','categories' ,'cast')
    
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment)