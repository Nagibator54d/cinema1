# movies/forms.py
from django import forms
from .models import Comment
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']



class SignUpForm(UserCreationForm):

    class Meta:
        model=User
        fields=(
            'username',
            'email',
            'password1',
            'password2',
        )