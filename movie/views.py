from django.shortcuts import render

# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Movie, Comment,Category
from .forms import CommentForm
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Movie

from django.http import JsonResponse
from .models import UserFavoriteMovies
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserFavoriteMovies

@csrf_exempt
@login_required
def add_to_favorites(request):
    if request.method == 'POST' and request.is_ajax():
        movie_id = request.POST.get('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        user = request.user

        favorites, created = UserFavoriteMovies.objects.get_or_create(user=user)
        
        if movie in favorites.movies.all():
            favorites.movies.remove(movie)
            status = 'removed'
        else:
            favorites.movies.add(movie)
            status = 'added'

        return JsonResponse({'status': status})

    return JsonResponse({'status': 'error'})

def remove_from_favorites(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        # Удаление фильма из избранного (адаптируйте под свою логику)
        request.user.favorite_movies.remove(movie)
        return HttpResponse({'status': 'removed'}, content_type='application/json')
    else:
        return HttpResponse(status=405)
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

@login_required

def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    genre_id = request.GET.get('genres')
    release_date = request.GET.get('release_date')
    p = Paginator(movies, 5)  # creating a paginator object
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
     
    if genre_id:
        movies = movies.filter(genre_id=genre_id)
    if release_date:
        movies = movies.filter(release_date=release_date)

    return render(request, 'movie_list.html', {
        'movies': movies,
        'categories': categories,
        'page_obj': page_obj
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.author = request.user
            comment.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = CommentForm()
    return render(request, 'movie_detail.html', {'movie': movie, 'comments': comments, 'form': form})

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
    
