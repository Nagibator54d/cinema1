from django.urls import reverse
from django.db import models
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

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField(auto_now=True)
    duration = models.PositiveIntegerField(help_text="Продолжительность в минутах")
    genres = models.ManyToManyField(Genre, related_name='movies')
    categories = models.ManyToManyField(Category, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='movies')
    cast = models.ManyToManyField(Actor, related_name='movies')
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Comment(models.Model):
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Используйте строку для избежания круговой зависимости
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

  # Переместите импорт User в конец файла, чтобы избежать круговой зависимости

class UserFavoriteMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')