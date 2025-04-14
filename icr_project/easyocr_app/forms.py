from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ImageUploadForm(forms.Form):
    image = forms.ImageField()



class CustomUserCreationForm(UserCreationForm):
    # Override fields to add placeholders
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')  # Include only the fields you want



#login logic

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password', 'class': 'form-control'})
    )