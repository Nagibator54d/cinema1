

# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignUpForm
from .models import Movie, Comment,Category,Genre,Series,Season,Episode
from .forms import CommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.http import JsonResponse

from .models import UserFavoriteMovies
from django.views.decorators.http import require_POST
import json
from django.core.mail import send_mail

def episode_detail(request, series_pk, season_pk, episode_pk):
    series = get_object_or_404(Series, pk=series_pk)
    season = get_object_or_404(Season, pk=season_pk)
    episode = get_object_or_404(Episode, pk=episode_pk)
    other_episodes = season.episodes.exclude(pk=episode_pk)

    context = {
        'series': series,
        'season': season,
        'episode': episode,
        'other_episodes': other_episodes,
    }
    return render(request, 'episode_detail.html', context)

def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    seasons = series.seasons.all()
    comments = Comment.objects.filter(series=series, parent=None)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.series = series
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect('series_detail', pk=series.pk)  # Corrected redirect

    return render(request, 'series_detail.html', {'series': series, 'seasons': seasons, 'comments': comments, 'form': form})



def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = Comment.objects.filter(movie=movie, parent=None)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect('movie_detail', pk=movie.pk)

    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments, 'form': form})
    
def episode_detail(request, series_pk, season_pk, episode_pk):
    series = get_object_or_404(Series, pk=series_pk)
    season = get_object_or_404(Season, pk=season_pk)
    episode = get_object_or_404(Episode, pk=episode_pk)
    other_episodes = season.episodes.exclude(pk=episode_pk)

    context = {
        'series': series,
        'season': season,
        'episode': episode,
        'other_episodes': other_episodes,
    }
    return render(request, 'episode_detail.html', context)

@login_required
def movie_play(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie_play.html', {'movie': movie})

def report_issue(request):
    if request.method == "POST":
        issue_description = request.POST['issue']
        send_mail(
            'Проблема с контентом',
            issue_description,
            'hadhdon1@gmail.com',
            ['hadhdon1@gmail.com'],
            fail_silently=False,
        )
        return redirect('movie_list')
    return redirect('movie_list')


def search_movies(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        series=Series.objects.filter(title__icontains=query)
        results = [{'id': movie.id, 'title': movie.title, 'poster': movie.poster.url} for movie in movies ]
    else:
        results = []
    return JsonResponse({'results': results})
@require_POST
@login_required
def add_to_favorites(request):
    movie_id = request.POST.get('movie_id')

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'Movie not found.'}), content_type='application/json', status=404)

    favorite, created = UserFavoriteMovies.objects.get_or_create(user=request.user, movie=movie)

    if created:
        return HttpResponse(json.dumps({'status': 'added'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'exists'}), content_type='application/json')



@require_POST
@login_required
def remove_from_favorites(request):
    movie_id = request.POST.get('movie_id')
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Movie not found.'}, status=404)

    favorite = UserFavoriteMovies.objects.filter(user=request.user, movie=movie)
    if favorite.exists():
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'not_found'}, status=404)



@login_required
def favorites(request):
    user = request.user
    favorite_movies = UserFavoriteMovies.objects.filter(user=user).select_related('movie')
    movies = [favorite_movie.movie for favorite_movie in favorite_movies]
    return render(request, 'favorites.html', {'favorite_movies': movies})

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('user_profile')
    return render(request, 'edit_profile.html')



def movie_list(request):
    movies = Movie.objects.all()
    series = Series.objects.all()
    categories = Category.objects.all()
    genres = Genre.objects.all()  # Получаем все жанры
    genre_id = request.GET.get('genres')
    release_date = request.GET.get('release_date')
    year = request.GET.get('year')

    if genre_id:
        series = series.filter(genres__id=genre_id)
        movies = movies.filter(genres__id=genre_id)  # Фильтруем по жанрам
        selected_genre = Genre.objects.get(id=genre_id)  # Получаем выбранный жанр
    else:
        selected_genre = None  # Если жанр не выбран

    if release_date:
        series = series.filter(release_date=release_date)
        movies = movies.filter(release_date=release_date)

    if year:
        movies = movies.filter(release_date__year=year)
        series = series.filter(release_date__year=year)   # Фильтруем по году

    # Получаем уникальные года
    years = Movie.objects.values_list('release_date__year', flat=True).distinct()

    p = Paginator(movies, 5)  # создаем объект пагинатора
    p1 = Paginator(series, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # возвращаем нужную страницу
        page_obj1 = p1.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
        page_obj1=p1.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
        page_obj1=p1.page(p1.num_pages)
    
    return render(request, 'movie_list.html', {
        'movies': movies,
        'series':series,
        'categories': categories,
        'genres': genres,  # Передаем жанры в шаблон
        'page_obj': page_obj,
        'page_obj1': page_obj1,
        'selected_genre': selected_genre,  # Передаем выбранный жанр в шаблон
        'selected_year': year,  # Передаем выбранный год в шаблон
        'years': years,
       # Передаем уникальные года в шаблон
    })





def category_filter(request, pk):
    category = get_object_or_404(Category, id=pk)
    movies = Movie.objects.filter(categories=category)
    return render(request, 'category.html', {'category': category, 'movies': movies})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):

    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            username=cd['username']
            password=cd['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
            return redirect('movie_list')
    else:
        form=AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
    
