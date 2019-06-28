from django import forms
from .models import Actor, Director, Movie

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor

        fields = [
            'name',
            'age',
        ]
        labels = {
            'name': 'Actor Name',
            'age': 'Age',
        }
        widgets = {
            'name': forms.TextInput(),
            'age': forms.NumberInput(),

        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = [
            'name',
            'age',
        ]
        labels = {
            'name': 'Director Name',
            'age': 'Age',
        }
        widgets = {
            'name': forms.TextInput(),
            'age': forms.NumberInput(),

        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title',
            'duration',
            'detail',
            'gender',
            'original_languaje',
            'country',
            'release_date',
            'poster',
            'trailer_url',
            'actors',
            'directors',
        ]
        labels = {
            'title': 'Movie Title',
            'duration': 'Movie Duration',
            'detail': 'Detail',
            'gender': 'Gender',
            'original_languaje': 'Original Languaje',
            'country': 'Country',
            'release_date': 'Realese Date',
            'poster': 'Poster',
            'trailer_url': 'Trailer URL',
            'actors': 'Actors',
            'directors': 'Directors',
        }
        widgets = {
            'title':forms.TextInput(attrs={'placeholder': 'Movie tittle','type' : 'text'}),
            'duration': forms.NumberInput(attrs={'placeholder': 'Movie tittle', 'type': 'tel'}),

        }


class MovieFormDownload(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Movie title', 'type': 'text'}))


class UserForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'username',
            'password1',
            'password2',

        ]
        label = {
            'username' : 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'type': 'password'}),
    )
