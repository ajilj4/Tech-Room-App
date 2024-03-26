from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):

    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1)
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}), min_length=1)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password (must be at least 8 characters)', widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)

    class Meta:
        model=User
        fields=['name','username','email','password1','password2']


class Roomform(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=["host","participants"]


class Userform(ModelForm):

    # avator = forms.FileField(label='Avator', widget=forms.FileInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1)
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1)
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=1)
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'class': 'form-control'}),min_length=10)


    class Meta:
        model=User
        fields=["avator","name","username","email","bio"]
       
        