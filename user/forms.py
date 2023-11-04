from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    password2 = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)