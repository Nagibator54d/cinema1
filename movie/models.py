from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=[self.id])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

class Screenwriter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сценаристы'
        verbose_name_plural = 'Сценаристы'

class Producer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продюссеры'
        verbose_name_plural = 'Продюссеры'

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField(auto_now=True)
    country=models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Продолжительность в минутах")
    genres = models.ManyToManyField(Genre, related_name='movies')
    categories = models.ManyToManyField(Category, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='movies')
    cast = models.ManyToManyField(Actor, related_name='movies')
    poster = models.ImageField(upload_to='posters/')
    video1 = models.FileField(upload_to='videos/', null=True, blank=True)  # Добавлено поле для видео
    video2 = models.FileField(upload_to='videos/', null=True, blank=True)  # Добавлено поле для видео
    video3 = models.FileField(upload_to='videos/', null=True, blank=True)  # Добавлено поле для видео
    screenwriter=models.ForeignKey(Screenwriter,on_delete=models.SET_NULL, null=True, related_name='movies')
    producer=models.ForeignKey(Producer,on_delete=models.SET_NULL, null=True, related_name='movies')
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = 'Фильмы'


class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/')
    genres = models.ManyToManyField(Genre, related_name='series')
    categories = models.ManyToManyField(Category, related_name='series')
    release_date = models.DateField(auto_now=True)
    country=models.CharField(max_length=200)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='series')
    cast = models.ManyToManyField(Actor, related_name='series')
    screenwriter=models.ForeignKey(Screenwriter,on_delete=models.SET_NULL, null=True, related_name='series')
    producer=models.ForeignKey(Producer,on_delete=models.SET_NULL, null=True, related_name='series')
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'

class Season(models.Model):
    series = models.ForeignKey(Series, related_name='seasons', on_delete=models.CASCADE)
    season_number = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.series.title} - Сезон {self.season_number}'

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

class Episode(models.Model):
    season = models.ForeignKey(Season, related_name='episodes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video1 = models.FileField(upload_to='episodes/', null=True , blank=True)
    video2 = models.FileField(upload_to='episodes/', null=True , blank=True)
    video3 = models.FileField(upload_to='episodes/', null=True , blank=True)
    episode_number = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.season.series.title} - Сезон {self.season.season_number} - Эпизод {self.episode_number}: {self.title}'

    class Meta:
        verbose_name = 'Эпизод'
        verbose_name_plural = 'Эпизоды'


class Comment(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class UserFavoriteMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    series=models.ForeignKey('Series', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie','series')


# Остальные модели остаются без изменений
