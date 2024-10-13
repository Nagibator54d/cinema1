# movies/admin.py
from django.contrib import admin
from .models import Genre, Director, Actor, Movie, Comment,Category,Screenwriter,Producer
from .models import Series, Season, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode

class SeasonAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]

admin.site.register(Series)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode)
# Остальные регистрации остаются без изменений


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration', 'director')
    search_fields = ('title',)
    list_filter = ('genres','categories','release_date')
    filter_horizontal = ('genres','categories' ,'cast')


admin.site.register(Screenwriter)    
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment)
admin.site.register(Producer)